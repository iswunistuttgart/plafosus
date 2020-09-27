import os
from django.core.exceptions import ValidationError


def validate_file_extension_3dpart(self):
    """
    Validator to check the file to be an 3d part.
    """
    ext = os.path.splitext(self.name)[1]  # [0] returns path+filename
    valid_extensions = ['.stl', '.obj', '.off', '.ply', '.3mf', '.xaml', '.3dxml', '.gltf']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension. Please upload a file with one of the following extensions: "
                              ".stl, .obj, .off, .ply, .3mf, .xaml, .3dxml, .gltf.")
