from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

# Core.
from core import models as core_models

# Model analysis.
import trimesh

# Calculation.
import json
import itertools
import uuid

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

    1. We search for the resources with skills,
    which match the required process step of a part manufacturing process step
    (resource_skill.skill.process_step == part_manufacturing_process_step.process_step).

    2. If constraints are defined, we check if the ability of the skill matches the constraint
    in dependence of the defined operator.

    3.
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

            # Add the manufacturing possibility number.
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

        logger.debug("Manufacturing possibilities before cleaning: " + str(manufacturing_possibilities))

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

        logger.debug("Manufacturing possibilities after cleaning: " + str(manufacturing_possibilities))

        # Calculate the costs (price, time and CO2) and consumables (in dependence which consumable exist)
        # for each single resource skill and subsequently for each solution
        # (unique combination of single resource skills for each manufacturing possibility).

        solution_space = []
        """List of all possible solutions (see below)."""

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

            for permutation in possible_permutations:
                i = 0
                """The current index of the possible_permutations list. 
                Used for finding the according part_manufacturing_process_step."""

                solution = {}
                """
                A solution is a unique combination of resource skills for one manufacturing possibility.
                Example:

                {   
                    "uuid": uuid.uuid4(),
                    "part": Part,
                    "manufacturing_possibility": manufacturing_possibility,
                    "price": "price in €",
                    "time": "time in s",
                    "co2": "co2 in co2-e",
                    "consumables": 
                        [
                            {
                                consumable: "name1",
                                quantity: "quantity2",
                                price: "price in €",
                                co2: "co2 in co2-e"
                            }
                        ],
                    "solution": [
                                    {
                                        "part_manufacturing_process_step": part_manufacturing_process_step1,
                                        "resource_skill": resource_skill,
                                        "price": "price in €",
                                        "time": "time in s",
                                        "co2":  "co2 in co2-e",
                                        "consumables": 
                                            [
                                                {
                                                    consumable: "name1",
                                                    quantity: "quantity2",
                                                    price: "price in €",
                                                    co2: "co2 in co2-e"
                                                }
                                            ]
                                    },   
                                    {
                                        "part_manufacturing_process_step": part_manufacturing_process_step2,
                                        "resource_skill": resource_skill,
                                        "price": "price in €",
                                        "time": "time in s",
                                        "co2":  "co2 in co2-e",
                                        "consumables": 
                                            [
                                                {
                                                    consumable: "name1",
                                                    quantity: "quantity2",
                                                    price: "price in €",
                                                    co2: "co2 in co2-e"
                                                }
                                            ]
                                    },   
                                ] 
                }       
                """

                # Initialization.
                solution["uuid"] = str(uuid.uuid4())
                solution["part"] = instance
                solution["manufacturing_possibility"] = manufacturing_possibility
                solution["price"] = 0
                solution["time"] = 0
                solution["co2"] = 0
                solution["consumables"] = []
                solution["solution"] = []

                # Initial meta data. Will be filled below.
                price_sum = 0
                time_sum = 0
                co2_sum = 0

                # Contains all consumables with the overall quantities.
                for consumable in core_models.Consumable.objects.all():
                    consumable_dict = {
                        "consumable": consumable,
                        "quantity": 0,
                        "price": 0,
                        "co2": 0
                    }
                    solution["consumables"].append(consumable_dict)

                for resource_skill in permutation:
                    # Calculate the meta data for this resource skill.
                    resource_skill_price = part_manufacturing_process_steps[
                                               i].required_quantity * resource_skill.quantity_price
                    price_sum = price_sum + resource_skill_price

                    resource_skill_time = part_manufacturing_process_steps[
                                              i].required_quantity * resource_skill.quantity_time
                    time_sum = time_sum + resource_skill_time

                    resource_skill_co2 = part_manufacturing_process_steps[
                                             i].required_quantity * resource_skill.quantity_co2
                    co2_sum = co2_sum + resource_skill_co2

                    # Add the consumables for one resource skill.
                    consumables = []
                    # Get all registered consumables.
                    for consumable in core_models.Consumable.objects.all():
                        # Check if this consumable is defined in the resource_skill.
                        if consumable in resource_skill.consumables.all():
                            consumable_quantity = resource_skill.SkillConsumable.all().get(
                                consumable=consumable).quantity * part_manufacturing_process_steps[
                                                   i].required_quantity

                            consumable_price = resource_skill.SkillConsumable.all().get(
                                consumable=consumable).quantity * part_manufacturing_process_steps[
                                                   i].required_quantity * resource_skill.SkillConsumable.all().get(
                                consumable=consumable).quantity_price

                            consumable_co2 = resource_skill.SkillConsumable.all().get(
                                consumable=consumable).quantity * part_manufacturing_process_steps[
                                                   i].required_quantity * resource_skill.SkillConsumable.all().get(
                                consumable=consumable).quantity_co2
                        else:
                            consumable_quantity = 0
                            consumable_price = 0
                            consumable_co2 = 0

                        consumable_dict = {
                            "consumable": consumable,
                            "quantity": consumable_quantity,
                            "price": consumable_price,
                            "co2": consumable_co2
                        }
                        # Add the consumable to the consumable list of this resource skill.
                        consumables.append(consumable_dict)

                        # Add the calculated meta data of the consumable to the overall sums.
                        price_sum = price_sum + consumable_price
                        co2_sum = co2_sum + consumable_co2

                        # Add the calculated meta data to the overall consumables overview.
                        updated_consumable = {}
                        for j in range(len(solution["consumables"])):
                            if solution["consumables"][j]['consumable'] == consumable:
                                updated_consumable["consumable"] = solution["consumables"][
                                                                    j]["consumable"]
                                updated_consumable["quantity"] = solution["consumables"][
                                                                    j]["quantity"] + consumable_quantity
                                updated_consumable["price"] = solution["consumables"][
                                                                    j]["price"] + consumable_price
                                updated_consumable["co2"] = solution["consumables"][
                                                                    j]["co2"] + consumable_co2
                                # Replace the old entry with the updated dict.
                                solution["consumables"][j] = updated_consumable

                    resource_skill_solution = {
                        "part_manufacturing_process_step": part_manufacturing_process_steps[i],
                        "manufacturing_sequence_number": part_manufacturing_process_steps[
                            i].manufacturing_sequence_number,
                        "resource_skill": resource_skill,
                        "price": resource_skill_price,
                        "time": resource_skill_time,
                        "co2": resource_skill_co2,
                        "consumables": consumables
                    }
                    # Add entry of this resource skill to the solution list.
                    solution["solution"].append(resource_skill_solution)
                    i = i + 1

                # Add the calculated sums to the solution dict.
                solution["price"] = price_sum
                solution["time"] = time_sum
                solution["co2"] = co2_sum

                # Add the created solution to the overall list.
                solution_space.append(solution)

        logger.debug("Solution space: " + str(solution_space))
        # Compare the single manufacturing_possibilities.

    except Exception as e:
        logger.error("Could not do the magic for part '{0}'.".format(str(instance.pk)), exc_info=True)
