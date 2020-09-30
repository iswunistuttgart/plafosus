from django.db.models.signals import post_save
from django.dispatch import receiver
from core import models
import logging

# Model analysis.
import trimesh


logger = logging.getLogger(__name__)


@receiver(post_save, sender=models.Part)
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


@receiver(post_save, sender=models.Part)
def select_machines_to_manufacture(sender, instance, created, **kwargs):
    """

    This function gets triggered when a part object is uploaded/saved
    and selects the 'best' machines to manufacture the part.
    """
    try:
        pass
        # TODO
    except Exception as e:
        logger.error("Could not select the best machines to manufacture the part.", exc_info=True)
