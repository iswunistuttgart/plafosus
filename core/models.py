from django.db import models
from django.urls import reverse
import uuid
from eopp import validations
from django.core.validators import MinValueValidator


# Method for uploading parts.
def model_upload_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/<filename>
    return 'uploads/parts/{0}'.format(filename)


class Part(models.Model):
    """
    The uploaded 3d part of the session.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    part = models.FileField(upload_to=model_upload_path,
                            validators=[validations.validate_file_extension_3dpart],
                            help_text="The uploaded 3d part.")

    # 3D part properties.
    is_valid = models.BooleanField(default=False,
                                   help_text="Is the 3d part valid (a closed/watertight 3d part).",
                                   editable=False)
    volume = models.FloatField(validators=[MinValueValidator(0)],
                               help_text="Volume of the part.",
                               blank=True,
                               null=True,
                               editable=False)
    bounding_box_x = models.FloatField(validators=[MinValueValidator(0)],
                                       help_text="Length (x-axis) of the bounding box of the part.",
                                       blank=True,
                                       null=True,
                                       editable=False)
    bounding_box_y = models.FloatField(validators=[MinValueValidator(0)],
                                       help_text="Width (y-axis) of the bounding box of the part.",
                                       blank=True,
                                       null=True,
                                       editable=False)
    bounding_box_z = models.FloatField(validators=[MinValueValidator(0)],
                                       help_text="Height (z-axis) of the bounding box of the part.",
                                       blank=True,
                                       null=True,
                                       editable=False)

    # Required skills to manufacture the part.
    # TODO

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('part-detail', args=[str(self.id)])


class Skill(models.Model):
    """
    An base skill.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=254,
                            help_text="The skill name.")
    description = models.CharField(max_length=254,
                                   help_text="Description of the skill.",
                                   blank=True)
    quantity_description = models.CharField(max_length=254,
                                            help_text="Description of the skill quantity (e.g. unit).",
                                            blank=True)

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('skill-detail', args=[str(self.id)])


class Machine(models.Model):
    """
    Machine.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=254,
                            help_text="The machine name.",
                            unique=True)
    manufacturer = models.CharField(max_length=254,
                                    help_text="Manufacturer of the machine.",
                                    blank=True)
    description = models.CharField(max_length=254,
                                   help_text="Description of the machine e.g. machine type.",
                                   blank=True)

    # Machine properties.
    build_space_x = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                help_text="Build space in x-axis in mm.",
                                                default=0)
    build_space_y = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                help_text="Build space in y-axis in mm.",
                                                default=0)
    build_space_z = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                help_text="Build space in z-axis in mm.",
                                                default=0)

    # Skills of the machine.
    skills = models.ManyToManyField(Skill,
                                    through='AppliedSkill',
                                    related_name='Machines',
                                    help_text="Skills of the machine.")

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('machine-detail', args=[str(self.id)])


class AppliedSkill(models.Model):
    """
    Through model for a specific skill of a machine.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    skill = models.ForeignKey(Skill,
                              on_delete=models.CASCADE,
                              related_name='AppliedSkill')
    machine = models.ForeignKey(Machine,
                                on_delete=models.CASCADE,
                                related_name='AppliedSkill')

    # Costs per skill quantity. TODO: specify the costs (€, CO2, ...)
    quantity_costs = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                 help_text="The costs to use the skill for one unit of the skill "
                                                           "specific quantity.",
                                                 default=0)

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['machine']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('appliedskill-detail', args=[str(self.id)])
