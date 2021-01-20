from django.db import models
from django.urls import reverse
import uuid
from eopp import validations
from django.core.validators import MinValueValidator, MaxValueValidator

# Third party packages
from django_countries.fields import CountryField

# Constants
MANUFACTURING_PROCESSES = (
    ('Primary shaping', 'Primary shaping'),
    ('Forming', 'Forming'),
    ('Separation', 'Separation'),
    ('Joining', 'Joining'),
    ('Coating', 'Coating'),
    ('Changing material properties', 'Changing material properties'),
)

OPERATORS = (
    ('=', '='),
    ('!=', '!='),
    ('<', '<'),
    ('>', '>'),
    ('>=', '>='),
    ('<=', '<='),
)

DATATYPES = (
    ('str', 'str'),
    ('bool', 'bool'),
    ('int', 'int'),
    ('float', 'float'),
)


# Method for uploading parts.
def model_upload_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/<filename>
    return 'uploads/parts/{0}'.format(filename)


class Unit(models.Model):
    """
    Unit of a requirement or a skill.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=254,
                            help_text="The unit name.",
                            unique=True)
    description = models.CharField(max_length=254,
                                   help_text="Description of the unit.",
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
        return reverse('unit-detail', args=[str(self.id)])


class Category(models.Model):
    """
    Category of a requirement.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=254,
                            help_text="The category name.",
                            unique=True)
    description = models.CharField(max_length=254,
                                   help_text="Description of the category.",
                                   blank=True)

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])


class ProcessStep(models.Model):
    """
    Generic representation of a manufacturing process (DIN 8580).
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    manufacturing_process = models.CharField(max_length=50,
                                             choices=MANUFACTURING_PROCESSES,
                                             help_text="The manufacturing process according to DIN 8580.")
    description = models.CharField(max_length=254,
                                   help_text="Description of the manufacturing process.",
                                   blank=True)
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             related_name='ProcessStep',
                             help_text="The unit of the process step.")

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['manufacturing_process']
        unique_together = [['manufacturing_process', 'unit']]

    def __str__(self):
        return self.manufacturing_process + " [" + self.unit.name + "]"

    def get_absolute_url(self):
        return reverse('processstep-detail', args=[str(self.id)])


class Skill(models.Model):
    """
    A skill is the general capability of a resource to perform a certain process step.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=254,
                            help_text="The skill name.")
    description = models.CharField(max_length=254,
                                   help_text="Description of the skill.",
                                   blank=True)

    process_step = models.ForeignKey(ProcessStep,
                                     on_delete=models.CASCADE,
                                     related_name='Skill')

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
    A part is the abstract description of an object to be manufactured.
    The object is defined by process steps and constraints
    (which are in combination a part manufacturing process step) to be performed.
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
                               help_text="Volume of the part in mm³.",
                               blank=True,
                               null=True,
                               editable=False)
    bounding_box_x = models.FloatField(validators=[MinValueValidator(0)],
                                       help_text="Length (x-axis) of the bounding box of the part in mm.",
                                       blank=True,
                                       null=True,
                                       editable=False)
    bounding_box_y = models.FloatField(validators=[MinValueValidator(0)],
                                       help_text="Width (y-axis) of the bounding box of the part in mm.",
                                       blank=True,
                                       null=True,
                                       editable=False)
    bounding_box_z = models.FloatField(validators=[MinValueValidator(0)],
                                       help_text="Height (z-axis) of the bounding box of the part in mm.",
                                       blank=True,
                                       null=True,
                                       editable=False)
    evaluation_method = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)],
                                            help_text="The evaluation method. "
                                                      "1: Ranking regarding single field values (e.g. price). "
                                                      "The highest importance weight is considered first. "
                                                      "2: Ranking regarding normalized and weighted criteria "
                                                      "(price, time and co2). "
                                                      "3: Ranking using the CRITIC method. "
                                                      "The importance weights are not considered.",
                                            default=3)
    price_importance = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                           help_text="The importance (weight) of the price for the "
                                                     "evaluation of the solutions. "
                                                     "Only used for evaluation method '2'.",
                                           default=1)
    time_importance = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                          help_text="The importance (weight) of the time for the "
                                                    "evaluation of the solutions. "
                                                    "Only used for evaluation method '2'.",
                                          default=1)
    co2_importance = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                         help_text="The importance (weight) of the co2 for the "
                                                   "evaluation of the solutions. "
                                                   "Only used for evaluation method '2'.",
                                         default=1)

    # Required skills to manufacture the part.
    process_steps = models.ManyToManyField(ProcessStep,
                                           through='PartManufacturingProcessStep',
                                           related_name='Parts',
                                           help_text="Required skills to manufacture the part.")

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

    def save(self, *args, **kwargs):
        self.volume = round(self.volume, 3)
        self.bounding_box_x = round(self.bounding_box_x, 3)
        self.bounding_box_y = round(self.bounding_box_y, 3)
        self.bounding_box_z = round(self.bounding_box_z, 3)
        super(Part, self).save(*args, **kwargs)


class Resource(models.Model):
    """
    A resource is an abstract representation of a machine or similar object in a production environment,
    which has the skills (with abilities and skill consumables) to perform part manufacturing process steps.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=254,
                            help_text="The resource name.",
                            unique=True)
    manufacturer = models.CharField(max_length=254,
                                    help_text="Manufacturer of the resource.",
                                    blank=True)
    description = models.CharField(max_length=254,
                                   help_text="Description of the resource e.g. machine type.",
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

    # Skills of the resource.
    skills = models.ManyToManyField(Skill,
                                    through='ResourceSkill',
                                    related_name='Resource',
                                    help_text="Skills of the resource.")

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
        return reverse('resource-detail', args=[str(self.id)])


class Consumable(models.Model):
    """
    A consumable is the abstract representation of a medium consumed by a resource to perform a skill (ResourceSkill).
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=254,
                            help_text="The consumable name.",
                            unique=True)
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             related_name='Consumable',
                             help_text="The unit of the consumable.")
    description = models.CharField(max_length=254,
                                   help_text="Description of the consumable.",
                                   blank=True)

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('consumable-detail', args=[str(self.id)])


class Requirement(models.Model):
    """
    A requirement describes abstract properties (without defining a specific value)
    of part manufacturing process steps (constraints) or skills (abilities).

    E.g. the requirement is 'material' -
    the constraint of the part is consequently material = metal,
    and a resource has the ability to process the material = metal.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=254,
                            help_text="The requirement name.",
                            unique=True)
    description = models.CharField(max_length=254,
                                   help_text="Specific description of the requirement.",
                                   blank=True)
    data_type = models.CharField(max_length=50,
                                 choices=DATATYPES,
                                 default="str",
                                 help_text="The data type of the value.")
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             related_name='Requirement',
                             help_text="The unit of the Requirement.")
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='Requirement',
                                 help_text="The category of the requirement.")

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('requirement-detail', args=[str(self.id)])


class ResourceSkill(models.Model):
    """
    Through model for a specific skill of a resource.

    The resource skill is a specific skill of a resource. Resource skills can have specific abilities.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    skill = models.ForeignKey(Skill,
                              on_delete=models.CASCADE,
                              related_name='ResourceSkill')
    resource = models.ForeignKey(Resource,
                                 on_delete=models.CASCADE,
                                 related_name='ResourceSkill')
    description = models.CharField(max_length=254,
                                   help_text="Specific description of the resource skill "
                                             "(e.g. level/quality of the skill).",
                                   blank=True)
    # Fixed costs.
    fixed_price = models.FloatField(validators=[MinValueValidator(0)],
                                    help_text="The fixed costs in € to use the skill.",
                                    default=0)
    fixed_time = models.FloatField(validators=[MinValueValidator(0)],
                                   help_text="The fixed time in s to use the skill "
                                             "(e.g. initial machine preparation).",
                                   default=0)
    fixed_co2 = models.FloatField(help_text="The fixed CO2-e to use the skill.",
                                  default=0)
    # Variable costs.
    variable_price = models.FloatField(validators=[MinValueValidator(0)],
                                       help_text="The variable costs in € to use the skill.",
                                       default=0)
    variable_time = models.FloatField(validators=[MinValueValidator(0)],
                                      help_text="The variable time in s to use the skill.",
                                      default=0)
    variable_co2 = models.FloatField(help_text="The variable CO2-e to use the skill.",
                                     default=0)

    consumables = models.ManyToManyField(Consumable,
                                         through='SkillConsumable',
                                         related_name='ResourceSkill',
                                         help_text="Consumables of the specific resource skill.")

    abilities = models.ManyToManyField(Requirement,
                                       through='Ability',
                                       related_name='ResourceSkill',
                                       help_text="Abilities of the specific resource skill.")

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['resource']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('resourceskill-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.fixed_price = round(self.fixed_price, 3)
        self.fixed_time = round(self.fixed_time, 3)
        self.fixed_co2 = round(self.fixed_co2, 3)
        self.variable_price = round(self.variable_price, 3)
        self.variable_time = round(self.variable_time, 3)
        self.variable_co2 = round(self.variable_co2, 3)
        super(ResourceSkill, self).save(*args, **kwargs)


class SkillConsumable(models.Model):
    """
    Through model for the required consumables for applying a specific skill of a specific resource (ResourceSkill).

    Skill consumables are the specific consumables (with defined quantities per unit)
    required by skill to perform his abilities.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    resource_skill = models.ForeignKey(ResourceSkill,
                                       on_delete=models.CASCADE,
                                       related_name='SkillConsumable')
    consumable = models.ForeignKey(Consumable,
                                   on_delete=models.CASCADE,
                                   related_name='SkillConsumable')
    description = models.CharField(max_length=254,
                                   help_text="Specific description of the used consumable.",
                                   blank=True)
    variable_quantity = models.FloatField(validators=[MinValueValidator(0)],
                                          help_text="The quantity required in the consumable unit "
                                                    "to use the skill for one unit.",
                                          default=0)
    fixed_quantity = models.FloatField(validators=[MinValueValidator(0)],
                                       help_text="The quantity required in the consumable unit "
                                                 "to use the skill.",
                                       default=0)
    # Fixed costs.
    fixed_price = models.FloatField(validators=[MinValueValidator(0)],
                                    help_text="The fixed costs in € for this consumable.",
                                    default=0)
    fixed_co2 = models.FloatField(help_text="The fixed CO2-e for this consumable.",
                                  default=0)
    # Variable Costs.
    variable_price = models.FloatField(validators=[MinValueValidator(0)],
                                       help_text="The variable costs in € for one unit of this consumable.",
                                       default=0)
    variable_co2 = models.FloatField(help_text="The variable CO2-e for one unit of this consumable.",
                                     default=0)

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
        return reverse('skillconsumable-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.variable_quantity = round(self.variable_quantity, 3)
        self.fixed_quantity = round(self.fixed_quantity, 3)
        self.fixed_price = round(self.fixed_price, 3)
        self.fixed_co2 = round(self.fixed_co2, 3)
        self.variable_price = round(self.variable_price, 3)
        self.variable_co2 = round(self.variable_co2, 3)
        super(SkillConsumable, self).save(*args, **kwargs)


class Ability(models.Model):
    """
    Through model for a specific ability of a skill.

    The ability of a skill is the possibility of a resource to fulfill requirements to a certain level/value.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    requirement = models.ForeignKey(Requirement,
                                    on_delete=models.CASCADE,
                                    related_name='Ability')
    resource_skill = models.ForeignKey(ResourceSkill,
                                       on_delete=models.CASCADE,
                                       related_name='Ability')
    description = models.CharField(max_length=254,
                                   help_text="Specific description of the ability.",
                                   blank=True)
    value = models.CharField(max_length=254,
                             help_text="Value of the specific requirement describing "
                                       "how much this requirement can be fulfilled. "
                                       "Please see the description and unit of the selected "
                                       "requirement for information.",
                             blank=False,)
    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Abilities"

    def clean(self):
        validations.validate_data_type_of_value(self)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('ability-detail', args=[str(self.id)])


class PartManufacturingProcessStep(models.Model):
    """
    Through model for a specific process step of a part.

    A process step with specific constraints to create a part.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    part = models.ForeignKey(Part,
                             on_delete=models.CASCADE,
                             related_name='PartManufacturingProcessStep')
    process_step = models.ForeignKey(ProcessStep,
                                     on_delete=models.CASCADE,
                                     related_name='PartManufacturingProcessStep')
    description = models.CharField(max_length=254,
                                   help_text="Description of the manufacturing step.",
                                   blank=True)

    # Costs per skill quantity.
    required_quantity = models.FloatField(validators=[MinValueValidator(0)],
                                          help_text="The required quantity of this process step to "
                                                    "manufacture the part.",
                                          default=0)

    manufacturing_possibility = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                            help_text="The number of the manufacturing "
                                                                      "possibility this process step belongs to.",
                                                            default=1)
    manufacturing_sequence_number = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                                help_text="The number of the manufacturing "
                                                                          "sequence this process step belongs to. "
                                                                          "Starting from 1.",
                                                                default=1)

    constraints = models.ManyToManyField(Requirement,
                                         through='Constraint',
                                         related_name='PartManufacturingProcessStep',
                                         help_text="Constraints of the specific part manufacturing process step.")

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['-created_at']
        unique_together = [['manufacturing_possibility', 'manufacturing_sequence_number']]

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('partmanufacturingprocessstep-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.required_quantity = round(self.required_quantity, 3)
        super(PartManufacturingProcessStep, self).save(*args, **kwargs)


class Constraint(models.Model):
    """
    A constraint is the specific requirement of a part manufacturing process step, which has to be fulfilled.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    requirement = models.ForeignKey(Requirement,
                                    on_delete=models.CASCADE,
                                    related_name='Constraint')
    part_manufacturing_process_step = models.ForeignKey(PartManufacturingProcessStep,
                                                        on_delete=models.CASCADE,
                                                        related_name='Constraint')
    description = models.CharField(max_length=254,
                                   help_text="Specific description of the constraint.",
                                   blank=True)
    value = models.CharField(max_length=254,
                             help_text="Value of the specific requirement describing "
                                       "how much this requirement has to be fulfilled. "
                                       "Please see the description and unit of the selected "
                                       "requirement for information.",
                             blank=False)
    operator = models.CharField(max_length=50,
                                choices=OPERATORS,
                                default="=",
                                help_text="Has the result to be equal, smaller, or bigger then this value.")
    optional = models.BooleanField(default=False,
                                   help_text="The optional flag is used, when one requirement must be met "
                                             "by a selection of several identical requirements. "
                                             "E.g. material can be plastic OR metal. "
                                             "If only one requirement is optional and their are no alternatives, "
                                             "it is handled like a 'normal' requirement, which has to be fulfilled.")

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)

    def clean(self):
        validations.validate_data_type_of_value(self)

    def get_absolute_url(self):
        return reverse('constraint-detail', args=[str(self.id)])
