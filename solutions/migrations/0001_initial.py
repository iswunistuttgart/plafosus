# Generated by Django 3.1.1 on 2020-11-26 13:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumableCost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_overall', models.BooleanField(default=False, help_text='Is this an overall consumable overview?')),
                ('quantity', models.DecimalField(decimal_places=3, default=0, help_text='The quantity in consumable unit.', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.DecimalField(decimal_places=3, default=0, help_text='The costs in € for this consumable.', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('co2', models.DecimalField(decimal_places=3, default=0, help_text='The co2-e for this consumable.', max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('consumable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ConsumableCost', to='core.consumable')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Permutation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rank', models.PositiveIntegerField(default=0, help_text='The rank of this permutation after evaluation.', validators=[django.core.validators.MinValueValidator(0)])),
                ('comparison_value', models.DecimalField(blank=True, decimal_places=3, help_text='The comparison value of this permutation.', max_digits=5, null=True)),
                ('manufacturing_possibility', models.PositiveIntegerField(help_text='The number of the manufacturing possibility the process steps belong to.', validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.DecimalField(decimal_places=3, default=0, help_text='The overall costs in € to manufacture the part.', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('time', models.DecimalField(decimal_places=3, default=0, help_text='The overall time in s to manufacture the part.', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('co2', models.DecimalField(decimal_places=3, default=0, help_text='The overall co2-e to manufacture the part.', max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('consumables', models.ManyToManyField(blank=True, help_text='Overall required consumables for this permutation.', related_name='Permutation', to='solutions.ConsumableCost')),
            ],
            options={
                'ordering': ('rank', '-created_at'),
            },
        ),
        migrations.CreateModel(
            name='SolutionSpace',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Permutation', to='core.part')),
                ('permutations', models.ManyToManyField(blank=True, help_text='All permutations for this solution space.', related_name='SolutionSpace', to='solutions.Permutation')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('manufacturing_sequence_number', models.PositiveIntegerField(help_text='The sequence number of the part manufacturing process step.', validators=[django.core.validators.MinValueValidator(0)])),
                ('quantity', models.DecimalField(decimal_places=3, default=0, help_text='The required quantity in the skill unit to manufacture the part.', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.DecimalField(decimal_places=3, default=0, help_text='The overall costs in € to manufacture the part.', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('time', models.DecimalField(decimal_places=3, default=0, help_text='The overall time in s to manufacture the part.', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('co2', models.DecimalField(decimal_places=3, default=0, help_text='The overall co2-e to manufacture the part.', max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('consumables', models.ManyToManyField(blank=True, help_text='Required consumables for this permutation.', related_name='Solution', to='solutions.ConsumableCost')),
                ('part_manufacturing_process_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Solution', to='core.partmanufacturingprocessstep')),
                ('resource_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Solution', to='core.resourceskill')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='permutation',
            name='solutions',
            field=models.ManyToManyField(blank=True, help_text='The resource skill for one part manufacturing process step.', related_name='Permutation', to='solutions.Solution'),
        ),
    ]
