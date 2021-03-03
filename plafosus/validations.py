import os
from django.core.exceptions import ValidationError


def validate_file_extension_3dpart(self):
    """
    Validator to check the file to be an 3d part.
    """
    ext = os.path.splitext(self.name)[1]  # [0] returns path+filename
    valid_extensions = ['.stl', '.obj', '.off', '.ply', '.3mf', '.xaml', '.3dxml', '.gltf']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension '{0}'. Please upload a file with one of the "
                              "following extensions: "
                              ".stl, .obj, .off, .ply, .3mf, .xaml, .3dxml, .gltf.".format(ext))


def validate_data_type_of_value(self):
    """
    Model validator to check if the conversion to the defined requirement data type is possible.
    """
    types = {
        'int': int,
        'float': float,
        'str': str,
        'bool': bool
    }
    try:
        value = types[self.requirement.data_type](self.value)
    except ValueError as e:
        raise ValidationError("Given value can not be converted to data type {0}."
                              .format(self.requirement.data_type))
