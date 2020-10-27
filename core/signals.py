from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

# Core.
from core import models as core_models

# Model analysis.
import trimesh

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
    This function gets triggered when a part object is uploaded/saved
    and selects the 'best' machines to manufacture the part.
    """
    try:
        possible_resources = {}
        """Dictionary containing each part_manufacturing_process_step as key and 
        as value a list with the resources, which fulfill all constraints."""

        manufacturing_possibilities = []
        """List containing all manufacturing possibilities."""

        # Get all through models 'PartManufacturingProcessStep' of the Part.
        for part_manufacturing_process_step in instance.PartManufacturingProcessStep.all():
            resources_temp = []
            """List temporarily containing the resources, 
            which fulfill all constraints of a part manufacturing process step."""

            # Add the manufacturing possibility number to a list.
            if part_manufacturing_process_step.manufacturing_possibility not in manufacturing_possibilities:
                manufacturing_possibilities.append(part_manufacturing_process_step.manufacturing_possibility)
            # Get all available resources.
            for resource in core_models.Resource.objects.all():
                # Get all through models 'ResourceSkill' of the Resource.
                for resource_skill in resource.ResourceSkill.all():
                    # Check if process_step of the resource_skill skill matches the process_step of
                    # the part_manufacturing_process_step.
                    if resource_skill.skill.process_step == part_manufacturing_process_step.process_step:
                        # Check if the resource_skill abilities fulfill the constraints of
                        # the part_manufacturing_process_step.
                        constraints_fulfilled = []
                        """List containing booleans, which indicate if all constraints of a 
                        part manufacturing process step were fulfilled. 
                        If there is a 'False' not all constraints could be fulfilled."""
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
                                        if constraint.value == ability.value:
                                            fulfilled = True
                                            break
                                    elif constraint.operator == "!=":
                                        if constraint.value != ability.value:
                                            fulfilled = True
                                            break
                                    elif constraint.operator == "<":
                                        if constraint.value < ability.value:
                                            fulfilled = True
                                            break
                                    elif constraint.operator == ">":
                                        if constraint.value > ability.value:
                                            fulfilled = True
                                            break
                                    elif constraint.operator >= "<=":
                                        if constraint.value <= ability.value:
                                            fulfilled = True
                                            break
                                    elif constraint.operator == ">=":
                                        if constraint.value >= ability.value:
                                            fulfilled = True
                                            break
                                    else:
                                        # Operator does not exist.
                                        # This should never happen, since the operators are fixed.
                                        pass

                            # Check if there was at least one ability, which fulfills the constraint.
                            if fulfilled:
                                constraints_fulfilled.append(True)
                            else:
                                constraints_fulfilled.append(False)
                                break

                        # Save this resource if it does not already exist and the constraints are fulfilled.
                        if False not in constraints_fulfilled and resource not in resources_temp:
                            resources_temp.append(resource)

            possible_resources[part_manufacturing_process_step] = resources_temp

        print(str(possible_resources))

        # Now check if there is a solution.
        # So at least one manufacturing_possibility, where every manufacturing_sequence_number has
        # at least one resource, which fulfills all constraints.
        for part_manufacturing_process_step, resources in possible_resources.items():
            if not resources:
                manufacturing_possibilities.remove(part_manufacturing_process_step.manufacturing_possibility)

        if not manufacturing_possibilities:
            # There is no solution.
            # TODO: print error message.
            pass
        else:
            pass
            # TODO: Rank the resources regarding the lowest costs (time, price, co2).

    except Exception as e:
        logger.error("Could not do the magic for part '{0}'.".format(str(sender)), exc_info=True)
