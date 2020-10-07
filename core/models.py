from django.db import models
from django.urls import reverse
import uuid
from eopp import validations
from django.core.validators import MinValueValidator

# Third party packages
from django_countries.fields import CountryField

# Constants
MANUFACTURING_PROCESSES = (
    ('P', 'Primary shaping'),
    ('F', 'Forming'),
    ('S', 'Separation'),
    ('J', 'Joining'),
    ('C', 'Coating'),
    ('M', 'Changing material properties'),
)


# Method for uploading parts.
def model_upload_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/<filename>
    return 'uploads/parts/{0}'.format(filename)


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

    manufacturing_process = models.CharField(max_length=1,
                                             choices=MANUFACTURING_PROCESSES,
                                             help_text="The manufacturing process according to DIN 8580.")

    quantity_description = models.CharField(max_length=254,
                                            help_text="Description of the skill quantity (e.g. painting of 1 mm^2. "
                                                      "Using the quantity, we calculate the costs and CO2-e. "
                                                      "For example to paint 4 mm^2 the costs are "
                                                      "4*quantity_costs of the machine in €).")

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
    skills = models.ManyToManyField(MANUFACTURING_PROCESSES,
                                    through='PartManufacturingProcess',
                                    related_name='Parts',
                                    help_text="Required skills to manufacture the part.")

    # TODO: Add skill specific requirements. E.g. Oberflächengüte

    # TODO: Add component (Halbzeug) and component state (z.B: Oberflächengüte nach Schnitt)

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

    # Address
    postal_code = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                              help_text="Postal code.")
    street = models.CharField(max_length=254,
                              help_text="Street.")
    city = models.CharField(max_length=254,
                            help_text="City.")
    country = CountryField(blank_label='(Select your country)',
                           help_text="Country.")

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
                                    through='MachineSkill',
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


class Consumable(models.Model):
    """
    Consumable which can be required by a MachineSkill.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=254,
                            help_text="The consumable name.",
                            unique=True)
    unit = models.CharField(max_length=254,
                            help_text="The unit of the consumable.",
                            unique=True)
    description = models.CharField(max_length=254,
                                   help_text="Description of this consumable.",
                                   blank=True)

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('consumable-detail', args=[str(self.id)])


class Ability(models.Model):
    """
    TODO
    The ability of a MachineSkill to fulfill specific requirement (e.g. processable material).
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Abilities"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('ability-detail', args=[str(self.id)])


class Requirement(models.Model):
    """
    TODO
    Requirements of a PartManufacturingProcess which have to be fulfilled.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('requirement-detail', args=[str(self.id)])


class Constraint(models.Model):
    """
    TODO
    Eine ausschließende Anforderung (True/False). Brauchen wir das überhaupt?
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('constraint-detail', args=[str(self.id)])


class MachineSkill(models.Model):
    """
    Through model for a specific skill of a machine.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    skill = models.ForeignKey(Skill,
                              on_delete=models.CASCADE,
                              related_name='MachineSkill')
    machine = models.ForeignKey(Machine,
                                on_delete=models.CASCADE,
                                related_name='MachineSkill')
    description = models.CharField(max_length=254,
                                   help_text="Specific description of this machine skill "
                                             "(e.g. level/quality of the skill).",
                                   blank=True)
    # Costs per skill quantity.
    quantity_price = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                 help_text="The costs in € to use the skill for one unit of the"
                                                           "skill specific quantity.",
                                                 default=0)
    quantity_time = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                help_text="The required time in s to apply the skill for one unit "
                                                          "of the skill specific quantity.",
                                                default=0)
    quantity_co2 = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                               help_text="The required CO2-e to use the skill for one unit of the "
                                                         "skill specific quantity. Including required consumables.",
                                               default=0)

    consumables = models.ManyToManyField(Consumable,
                                         through='SkillConsumable',
                                         related_name='MachineSkill',
                                         help_text="Consumables of the specific machine skill.")
    # TODO
    ability = models.ManyToManyField(Ability,
                                     through='SkillAbility',
                                     related_name='MachineSkill',
                                     help_text="Abilities of the specific machine skill.")

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
        return reverse('machineskill-detail', args=[str(self.id)])


class SkillConsumable(models.Model):
    """
    Through model for the required consumables for applying a specific skill of a specific machine (MachineSkill).
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    machine_skill = models.ForeignKey(MachineSkill,
                                      on_delete=models.CASCADE,
                                      related_name='SkillConsumable')
    consumable = models.ForeignKey(Consumable,
                                   on_delete=models.CASCADE,
                                   related_name='SkillConsumable')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                           help_text="The required quantity of the consumable to "
                                                     "apply the skill.",
                                           default=0)

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('skillconsumable-detail', args=[str(self.id)])


class PartManufacturingProcess(models.Model):
    """
    Through model for a required specific manufacturing process of a part.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    manufacturing_process = models.CharField(max_length=1,
                                             choices=MANUFACTURING_PROCESSES,
                                             help_text="The manufacturing process according to DIN 8580.")
    part = models.ForeignKey(Part,
                             on_delete=models.CASCADE,
                             related_name='PartManufacturingProcess')
    description = models.CharField(max_length=254,
                                   help_text="Description of this manufacturing step.",
                                   blank=True)

    # Costs per skill quantity.
    required_quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                    help_text="The required quantity of the skill to "
                                                              "manufacture the part.",
                                                    default=0)

    manufacturing_possibility = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                            help_text="The number of the manufacturing "
                                                                      "possibility this skill belongs.",
                                                            default=1)
    manufacturing_sequence_number = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                                help_text="The number of the manufacturing "
                                                                          "sequence this skill belongs. "
                                                                          "Starting from 1.",
                                                                default=1)

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['part']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('partmanufacturingprocess-detail', args=[str(self.id)])


class SkillAbility(models.Model):
    """
    TODO
    Through model for a specific ability of a skill.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    ability = models.ForeignKey(Ability,
                                on_delete=models.CASCADE,
                                related_name='SkillAbility')
    machine_skill = models.ForeignKey(MachineSkill,
                                      on_delete=models.CASCADE,
                                      related_name='SkillAbility')

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "SkillAbilities"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('skillability-detail', args=[str(self.id)])
