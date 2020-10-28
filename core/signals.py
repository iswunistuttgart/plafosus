from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

# App imports.
from core import models as core_models
from solutions import models as solutions_models

# Model analysis.
import trimesh

# Calculation.
import json
import itertools

logger = logging.getLogger(__name__)


@receiver(post_save, sender=core_models.Part)
def analyze_part(sender, instance, created, **kwargs):
    """
    This function gets triggered when a part object is uploaded/saved
    and analyzes the part and fills the respective fields.

    Projects for analyzing meshes:

    - Trimesh:      https://github.com/mikedh/trimesh
    - Meshio:       https://github.com/nschloe/meshio
    - Open3D:       http://www.open3d.org/
    - PyMesh:       https://github.com/PyMesh/PyMesh
    - Numpy-STL:    https://github.com/WoLpH/numpy-stl/
    """
    if created:
        """        
        Import meshes from:
        - binary/ASCII STL
        - Wavefront OBJ
        - ASCII OFF
        - binary/ASCII PLY
        - GLTF/GLB 2.0
        - 3MF
        - XAML
        - 3DXML
        Import geometry files using the GMSH SDK if installed (BREP, STEP, IGES, INP, BDF, etc)
        """
        # TODO: Test different formats
        try:
            mesh = trimesh.load(str(instance.part.path))

            # Is the current mesh watertight?
            is_watertight = mesh.is_watertight
            instance.is_valid = is_watertight

            # Is the current mesh convex?
            """
            Convex is defined as:
            1) "Convex, meaning "curving out" or "extending outward" (compare to concave)
            2) having an outline or surface curved like the exterior of a circle or sphere.
            3) (of a polygon) having only interior angles measuring less than 180
            """
            is_convex = mesh.is_convex

            # The volume of the mesh in mm³.
            instance.volume = int(mesh.volume)

            # An axis aligned bounding box in mm.
            bounding_box_x, bounding_box_y, bounding_box_z = mesh.bounding_box.extents
            instance.bounding_box_x = round(bounding_box_x, 3)
            instance.bounding_box_y = round(bounding_box_y, 3)
            instance.bounding_box_z = round(bounding_box_z, 3)

            instance.save()

        except Exception as e:
            logger.error("Could not analyze and save information about 3d part in the data base.", exc_info=True)


@receiver(post_save, sender=core_models.Part)
def select_machines_to_manufacture(sender, instance, created, **kwargs):
    """
    TODO: I think this receives not the actual values (sometimes I have to save twice?).

    This function gets triggered when a part object is uploaded/saved
    and selects the 'best' machines to manufacture the part.

    1.  We search for the resources with skills,
        which match the required process step of a part manufacturing process step
        (resource_skill.skill.process_step == part_manufacturing_process_step.process_step).

    2.  If constraints are defined, we check if the ability of the skill matches the constraint
        in dependence of the defined operator.

    3.  Then we have the information for which part_manufacturing_process_step, which resources skill is possible
        (manufacturing_possibilities).

    4.  Using this information, we create all possible permutations. This means unique combinations of resource_skills.

    5.  Then we calculate the meta data (price, time, co2 etc) for each permutation.

    6.  Subsequently, we evaluate the single permutations.
    """
    try:
        possible_resource_skills = {}
        """
        Dictionary containing each part_manufacturing_process_step as key and 
        as value a list with the resource skills, which fulfill all constraints.
        This is required, because we can not directly pop a manufacturing_possibility from manufacturing_possibilities, 
        because this would change the size of the dict during the for loop (which is required for the check).         
        Example: 
        
        {
         part_manufacturing_process_step1: [resource_skill1, resource_skill2],
         
         part_manufacturing_process_step2: [resource_skill1]
        }
        """

        manufacturing_possibilities = {}
        """
        Contains all possible manufacturing possibilities and the according part manufacturing steps 
        with the possible resource skills.        
        Example: 
        
        {
         manufacturing_possibility1: 
            {
             part_manufacturing_process_step1: [resource_skill1, resource_skill2], 
             
             part_manufacturing_process_step2: [resource_skill1]
            }
        }
        """

        # Get all through models 'PartManufacturingProcessStep' of the Part.
        for part_manufacturing_process_step in instance.PartManufacturingProcessStep.all():
            resources_temp = []
            """
            List temporarily containing the resource skills, 
            which fulfill all constraints of a part manufacturing process step.
            """

            # Add the manufacturing possibility number and part_manufacturing_process_step.
            if part_manufacturing_process_step.manufacturing_possibility not in manufacturing_possibilities.keys():
                manufacturing_possibilities[part_manufacturing_process_step.manufacturing_possibility] = {
                    part_manufacturing_process_step: []}
            else:
                manufacturing_possibilities[part_manufacturing_process_step.manufacturing_possibility][
                    part_manufacturing_process_step] = []

            # Get all available resources.
            for resource in core_models.Resource.objects.all():
                # Get all through models 'ResourceSkill' of the Resource.
                for resource_skill in resource.ResourceSkill.all():
                    # Check if the resource_skill abilities fulfill the constraints of
                    # the part_manufacturing_process_step. If so, 'True' is added to this list. Otherwise, 'False'.
                    constraints_fulfilled = []
                    """List containing booleans, which indicate if all constraints of a 
                    part manufacturing process step were fulfilled. 
                    If there is a 'False' not all constraints could be fulfilled."""
                    # Check if process_step of the resource_skill skill matches the process_step of
                    # the part_manufacturing_process_step.
                    if resource_skill.skill.process_step == part_manufacturing_process_step.process_step:
                        for constraint in part_manufacturing_process_step.Constraint.all():
                            # Check if this constraint is optional.
                            optional = constraint.optional
                            """Is this constraint optional."""
                            fulfilled = False
                            """Is there an ability, which fulfills this constraint."""
                            for ability in resource_skill.Ability.all():
                                # Check if the ability is based on the same requirement as the constraint.
                                if ability.requirement == constraint.requirement:
                                    # Check if the value of the ability satisfies the value of the constraint
                                    # in dependence of the defined operator.
                                    if constraint.operator == "=":
                                        if ability.value == constraint.value:
                                            fulfilled = True
                                            break
                                    elif constraint.operator == "!=":
                                        if ability.value != constraint.value:
                                            fulfilled = True
                                            break
                                    elif constraint.operator == "<":
                                        if ability.value < constraint.value:
                                            fulfilled = True
                                            break
                                    elif constraint.operator == ">":
                                        if ability.value > constraint.value:
                                            fulfilled = True
                                            break
                                    elif constraint.operator >= "<=":
                                        if ability.value <= constraint.value:
                                            fulfilled = True
                                            break
                                    elif constraint.operator == ">=":
                                        if ability.value >= constraint.value:
                                            fulfilled = True
                                            break
                                    else:
                                        # Operator does not exist.
                                        # This should never happen, since the operators are fixed.
                                        logger.error("Could not find a matching operator for given operator '{0}' "
                                                     "of constraint '{1}'."
                                                     .format(str(constraint.operator), str(constraint)))

                            # Check if there was at least one ability, which fulfills the constraint.
                            if fulfilled:
                                constraints_fulfilled.append(True)
                            else:
                                constraints_fulfilled.append(False)
                                break

                        # Save this resource if it does not already exist and the constraints are fulfilled.
                        if False not in constraints_fulfilled:
                            resources_temp.append(resource_skill)

            # Add the list with possible resource skills to the possible_resource_skills dictionary.
            possible_resource_skills[part_manufacturing_process_step] = resources_temp
            # Add the list with possible resource skills to the manufacturing_possibilities dictionary.
            manufacturing_possibilities[part_manufacturing_process_step.manufacturing_possibility][
                part_manufacturing_process_step] = resources_temp

        # logger.debug("Manufacturing possibilities before cleaning: " + str(manufacturing_possibilities))

        # Now check if there is a solution.
        # So at least one manufacturing_possibility, where every manufacturing_sequence_number has
        # at least one resource (with an underlying resource_skill), which fulfills all constraints.
        for part_manufacturing_process_step, resource_skills in possible_resource_skills.items():
            if not resource_skills:
                logger.warning("Manufacturing possibility '{0}' of part '{1}' is not manufacturable, "
                               "since part manufacturing process step '{2}' with manufacturing sequence number '{3}' "
                               "has no resource with according resource skills, which fulfill the constraints."
                               .format(str(part_manufacturing_process_step.manufacturing_possibility),
                                       str(instance.pk),
                                       str(part_manufacturing_process_step.process_step),
                                       str(part_manufacturing_process_step.manufacturing_sequence_number)))
                # Remove complete manufacturing_possibility from dict.
                manufacturing_possibilities.pop(part_manufacturing_process_step.manufacturing_possibility, None)

        if not manufacturing_possibilities:
            # There is no solution.
            logger.error("Could not find a valid solution for part '{0}'. "
                         "There is no manufacturing possibility, where each part manufacturing process step "
                         "has a possible resource (with according resource skills), which fulfills the constraints."
                         .format(str(instance.pk)))
            return

        # logger.debug("Manufacturing possibilities after cleaning: " + str(manufacturing_possibilities))

        # Calculate the costs (price, time and CO2) and consumables (in dependence which consumable exist)
        # for each single resource skill and subsequently for each solution
        # (unique combination of single resource skills for each manufacturing possibility).

        solution_space = solutions_models.SolutionSpace.objects.create(part=instance)

        # Now we try to create and calculate the single solutions.
        for manufacturing_possibility, process_steps_with_resource_skills in manufacturing_possibilities.items():
            all_resource_skills_per_manufacturing_process_step = []
            """A list containing all lists with resource skills for each manufacturing process step 
            of a manufacturing possibility.
            Example:

            |------MPS1----|  |-----MPS2----|  |-----MPS3------|
            [[RS1, RS3, RS4], [RS6, RS7, RS9], [RS8, RS10, RS5]]
            """

            part_manufacturing_process_steps = []
            """List of all part_manufacturing_process_steps for this manufacturing possibility."""

            for part_manufacturing_process_step, resource_skills in process_steps_with_resource_skills.items():
                all_resource_skills_per_manufacturing_process_step.append(resource_skills)
                part_manufacturing_process_steps.append(part_manufacturing_process_step)

            # Calculate all possible permutations. Result is a list of tuples.
            # Since tuples are ordered, we can find the according part_manufacturing_process_step
            # on the same place in part_manufacturing_process_steps as the permutation in possible_permutations.
            possible_permutations = list(itertools.product(*all_resource_skills_per_manufacturing_process_step))
            """List of tuples, which represent the single permutations. 
            This means every combination of resource skills for each required part_manufacturing_process_step.
            Example:
            
            [(RS1, RS6, RS8), (RS1, RS6, RS10) ...]
            """

            # Iterate over all possible permutations.
            for possible_permutation in possible_permutations:
                i = 0
                """The current index of the set in the possible_permutations list. 
                Used for finding the according part_manufacturing_process_step."""

                # Create a new object for this permutation.
                permutation = solutions_models.Permutation(manufacturing_possibility=manufacturing_possibility)
                permutation.save()

                # Initial meta data of this permutation, which will be updated below.
                permutation_price = 0
                permutation_time = 0
                permutation_co2 = 0

                # Create a ConsumableCost object for each existing consumable.
                # These are the overall consumables of one permutation.
                overall_consumable = []
                """List containing all created ConsumableCost objects for this permutation."""
                for consumable_object in core_models.Consumable.objects.all():
                    # Create the ConsumableCost object.
                    consumable = solutions_models.ConsumableCost(consumable=consumable_object,
                                                                 is_overall=True)
                    consumable.save()

                    # Add the ConsumableCost object to the permutation.
                    permutation.consumables.add(consumable)

                    # Add the ConsumableCost object to a list, so we can update the objects,
                    # when we have calculated the ConsumableCost objects for each resource_skill.
                    overall_consumable.append(consumable)

                # Iterate over all resource_skills in the permutation.
                for resource_skill in possible_permutation:
                    # Calculate the meta data for this resource_skill.
                    resource_skill_price = part_manufacturing_process_steps[
                                               i].required_quantity * resource_skill.quantity_price
                    permutation_price = permutation_price + resource_skill_price

                    resource_skill_time = part_manufacturing_process_steps[
                                              i].required_quantity * resource_skill.quantity_time
                    permutation_time = permutation_time + resource_skill_time

                    resource_skill_co2 = part_manufacturing_process_steps[
                                             i].required_quantity * resource_skill.quantity_co2
                    permutation_co2 = permutation_co2 + resource_skill_co2

                    # Add the consumables for one resource_skill.
                    resource_skill_consumables = []
                    """List containing all ConsumableCost objects for one resource_skill."""
                    # Get all registered consumables.
                    for consumable_object in core_models.Consumable.objects.all():
                        # Check if this consumable is defined in the resource_skill.
                        if consumable_object in resource_skill.consumables.all():
                            # If yes, we calculate the meta data for this consumable.
                            consumable_quantity = resource_skill.SkillConsumable.all().get(
                                consumable=consumable_object).quantity * part_manufacturing_process_steps[
                                                   i].required_quantity

                            consumable_price = resource_skill.SkillConsumable.all().get(
                                consumable=consumable_object).quantity * part_manufacturing_process_steps[
                                                   i].required_quantity * resource_skill.SkillConsumable.all().get(
                                consumable=consumable_object).quantity_price

                            consumable_co2 = resource_skill.SkillConsumable.all().get(
                                consumable=consumable_object).quantity * part_manufacturing_process_steps[
                                                   i].required_quantity * resource_skill.SkillConsumable.all().get(
                                consumable=consumable_object).quantity_co2
                        else:
                            # Otherwise, we set everything 0.
                            consumable_quantity = 0
                            consumable_price = 0
                            consumable_co2 = 0

                        # Now we create a ConsumableCost object for each available consumable.
                        consumable = solutions_models.ConsumableCost(
                            consumable=consumable_object,
                            is_overall=False,
                            quantity=consumable_quantity,
                            price=consumable_price,
                            co2=consumable_co2)
                        consumable.save()
                        # Add the consumable to the consumable list of this resource_skill.
                        resource_skill_consumables.append(consumable)

                        # Add the calculated meta data of the consumable to the resource sums.
                        resource_skill_price = resource_skill_price + consumable_price
                        resource_skill_co2 = resource_skill_co2 + consumable_co2

                        # Add the calculated meta data of the consumable to the overall permutation sums.
                        permutation_price = permutation_price + consumable_price
                        permutation_co2 = permutation_co2 + consumable_co2

                        # Update the overall consumables.
                        for overall_consumable_object in overall_consumable:
                            if overall_consumable_object.consumable == consumable_object:
                                # Calculate the new values.
                                new_co2 = overall_consumable_object.co2 + consumable_co2
                                new_price = overall_consumable_object.price + consumable_price
                                new_quantity = overall_consumable_object.quantity + consumable_quantity
                                # Update the field values.
                                overall_consumable_object.quantity = new_quantity
                                overall_consumable_object.price = new_price
                                overall_consumable_object.co2 = new_co2
                                # Save the updated overall consumable.
                                overall_consumable_object.save()

                    # Create a new solution object (for each resource_skill).
                    solution = solutions_models.Solution(
                        part_manufacturing_process_step=part_manufacturing_process_steps[i],
                        resource_skill=resource_skill,
                        manufacturing_sequence_number=part_manufacturing_process_steps[i].manufacturing_sequence_number,
                        quantity=part_manufacturing_process_steps[i].required_quantity,
                        price=resource_skill_price,
                        time=resource_skill_time,
                        co2=resource_skill_co2)
                    solution.save()

                    # Add all consumables to the many2many field of the solution.
                    for consumable in resource_skill_consumables:
                        solution.consumables.add(consumable)

                    # Add the solution object to the permutation.
                    permutation.solutions.add(solution)

                    # Count further.
                    i += 1

                # Add the calculated sums to the permutation.
                permutation.price = permutation_price
                permutation.time = permutation_time
                permutation.co2 = permutation_co2
                # Save the permutation object.
                permutation.save()

                # Add the created permutation object to the solution_space.
                solution_space.permutations.add(permutation)

        # Call one of the evaluation methods, which rank the permutations.
        # TODO: The method to be used shall be defined in the part.
        method_number = 1
        if len(solution_space.permutations.all()) <= 1:
            logger.info("Could not evaluate the permutations, since there is only one.")
            field_evaluation(solution_space=solution_space,
                             fields=['price'])
        elif method_number == 1:
            weighted_field_evaluation(solution_space=solution_space,
                                      price_weight=solution_space.part.price_importance,
                                      time_weight=solution_space.part.time_importance,
                                      co2_weight=solution_space.part.co2_importance)
        else:
            logger.error("Given method_number '{0}' is not defined.".format(str(method_number)))

    except Exception as e:
        logger.error("Could not do the magic for part '{0}'.".format(str(instance.pk)), exc_info=True)


def field_evaluation(solution_space: solutions_models.SolutionSpace, fields: [str]):
    """
    Gives ranks to the permutations of a solution_space with regard to the value of the given fields.
    The order of given fields decides, which is the first, second etc. field to be evaluated.

    :param solution_space:  The solution space, which shall be evaluated.
    :param fields:  List of fields of the permutation, which shall be used for the evaluation.
                    Can be: 'price', 'time' or 'co2'. Add '-' of descending order e.g. '-price'.
    """
    try:
        # Order the permutations of the solution_space with the given fields.
        permutations = solution_space.permutations.all().order_by(*fields)

        i = 1
        """The rank number."""
        for permutation in permutations:
            # Write the ranks in dependence of the permutations queryset.
            permutation.rank = i
            permutation.save()
            i += 1

    except Exception as e:
        logger.error("Could not do execute the field evaluation for solution_space '{0}' and fields '{1}'."
                     .format(str(solution_space), str(fields)), exc_info=True)


def weighted_field_evaluation(solution_space: solutions_models.SolutionSpace,
                              price_weight: int, time_weight: int, co2_weight: int):
    """
    Gives ranks to the permutations of a solution_space with regard to the weighted value of the given fields.
    The order of given fields decides, which is the first, second etc. field to be evaluated.

    :param solution_space:  The solution space, which shall be evaluated.
    :param price_weight: The weights of the price.
    :param time_weight: The weights of the time.
    :param co2_weight: The weights of the co2.
    """
    try:
        # 1. Normalization:
        # Get the max and min value for price, time and co2 of all permutations.

        # Price.
        # First entry is the permutation with the minimal and the last with the maximal price.
        permutations_price = solution_space.permutations.all().order_by('price')
        price_min = permutations_price.first().price
        price_max = permutations_price.last().price

        # Time.
        # First entry is the permutation with the minimal and the last with the maximal time.
        permutations_time = solution_space.permutations.all().order_by('time')
        time_min = permutations_time.first().time
        time_max = permutations_time.last().time

        # CO2.
        # First entry is the permutation with the minimal and the last with the maximal co2.
        permutations_co2 = solution_space.permutations.all().order_by('co2')
        co2_min = permutations_co2.first().co2
        co2_max = permutations_co2.last().co2

        rank_values = []
        for permutation in permutations_price:
            # Calculate the normalized value and weight it for each permutation.
            price_norm = (permutation.price - price_min) / (price_max - price_min)
            price_weighted = price_norm * price_weight

            time_norm = (permutation.time - time_min) / (time_max - time_min)
            time_weighted = time_norm * time_weight

            co2_norm = (permutation.co2 - co2_min) / (co2_max - co2_min)
            co2_weighted = co2_norm * co2_weight

            value = sum([price_weighted, time_weighted, co2_weighted])
            rank_values.append(value)

        # Sort the permutation list in dependence of the rank_values.
        sorted_permutations = [x for _, x in sorted(zip(rank_values, list(permutations_price)))]

        i = 1
        """The rank number."""
        for permutation in sorted_permutations:
            # Write the ranks in dependence of the permutations queryset.
            permutation.rank = i
            permutation.save()
            i += 1

    except Exception as e:
        logger.error("Could not do execute the weighted field evaluation for solution_space '{0}'."
                     .format(str(solution_space)), exc_info=True)
