from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
import uuid

from core import models as core_models


class ConsumableCost(models.Model):
    """
    The costs of a consumable.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    consumable = models.ForeignKey(core_models.Consumable,
                                   on_delete=models.CASCADE,
                                   related_name='ConsumableCost')

    is_overall = models.BooleanField(help_text="Is this an overall consumable overview?",
                                     default=False)

    quantity = models.FloatField(validators=[MinValueValidator(0)],
                                 help_text="The quantity in consumable unit.",
                                 default=0)
    price = models.FloatField(help_text="The costs in € for this consumable.",
                              default=0)
    co2 = models.FloatField(help_text="The CO2-eq. for this consumable.",
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
        return reverse('consumablecost-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        """
        self.quantity = round(self.quantity, 3) if self.quantity else self.quantity
        self.price = round(self.price, 3) if self.price else self.price
        self.co2 = round(self.co2, 3) if self.co2 else self.co2
        """
        super(ConsumableCost, self).save(*args, **kwargs)


class Solution(models.Model):
    """
    One solution (combination of a part_process_step and resource_skill).
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    part_process_step = models.ForeignKey(core_models.PartProcessStep,
                                          on_delete=models.CASCADE,
                                          related_name='Solution')
    resource_skill = models.ForeignKey(core_models.ResourceSkill,
                                       on_delete=models.CASCADE,
                                       related_name='Solution')
    manufacturing_sequence_number = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                                help_text="The sequence number of the part "
                                                                          "process step.")
    quantity = models.FloatField(validators=[MinValueValidator(0)],
                                 help_text="The required quantity in the skill unit to manufacture the part.",
                                 default=0)
    price = models.FloatField(help_text="The overall costs in € to manufacture the part.",
                              default=0)
    time = models.FloatField(validators=[MinValueValidator(0)],
                             help_text="The overall time in s to manufacture the part.",
                             default=0)
    co2 = models.FloatField(help_text="The overall CO2-eq. to manufacture the part.",
                            default=0)
    consumables = models.ManyToManyField(ConsumableCost,
                                         related_name='Solution',
                                         help_text="Required consumables for this permutation.",
                                         blank=True)

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
        return reverse('solution-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        """
        self.quantity = round(self.quantity, 3) if self.quantity else self.quantity
        self.price = round(self.price, 3) if self.price else self.price
        self.time = round(self.time, 3) if self.time else self.time
        self.co2 = round(self.co2, 3) if self.co2 else self.co2
        """
        super(Solution, self).save(*args, **kwargs)


class Permutation(models.Model):
    """
    Permutation: A possible solution.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    rank = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                       help_text="The rank of this permutation after evaluation.",
                                       default=0)
    comparison_value = models.FloatField(help_text="The comparison value of this permutation.",
                                         blank=True,
                                         null=True)
    manufacturing_possibility = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                                            help_text="The number of the manufacturing "
                                                                      "possibility the process steps belong to.")
    price = models.FloatField(help_text="The overall costs in € to manufacture the part.",
                              default=0)
    time = models.FloatField(validators=[MinValueValidator(0)],
                             help_text="The overall time in s to manufacture the part.",
                             default=0)
    co2 = models.FloatField(help_text="The overall CO2-eq. to manufacture the part.",
                            default=0)
    consumables = models.ManyToManyField(ConsumableCost,
                                         related_name='Permutation',
                                         help_text="Overall required consumables for this permutation.",
                                         blank=True)
    solutions = models.ManyToManyField(Solution,
                                       related_name="Permutation",
                                       help_text="The resource skill for one part process step.",
                                       blank=True)

    # Meta.
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ('rank', '-created_at')

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('permutation-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.comparison_value = round(self.comparison_value, 3) if self.comparison_value else self.comparison_value
        """
        self.price = round(self.price, 3) if self.price else self.price
        self.time = round(self.time, 3) if self.time else self.time
        self.co2 = round(self.co2, 3) if self.co2 else self.co2
        """
        super(Permutation, self).save(*args, **kwargs)


class SolutionSpace(models.Model):
    """
    All permutations.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    part = models.ForeignKey(core_models.Part,
                             on_delete=models.CASCADE,
                             related_name='Permutation')
    permutations = models.ManyToManyField(Permutation,
                                          related_name="SolutionSpace",
                                          help_text="All permutations for this solution space.",
                                          blank=True)

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
        return reverse('solutionspace-detail', args=[str(self.id)])
