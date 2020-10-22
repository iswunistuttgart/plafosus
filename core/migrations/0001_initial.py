# Generated by Django 3.1.1 on 2020-10-22 09:08

import core.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import eopp.validations
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.CharField(help_text='Value of the specific requirement describing how much this requirement can be fulfilled. Please see the description and unit of the selected requirement for information.', max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Abilities',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The category name.', max_length=254, unique=True)),
                ('description', models.CharField(blank=True, help_text='Description of the category.', max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Constraint',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.CharField(help_text='Value of the specific requirement describing how much this requirement has to be fulfilled. Please see the description and unit of the selected requirement for information.', max_length=254)),
                ('operator', models.CharField(choices=[('=', '='), ('<', '<'), ('!=', '!='), ('>', '>'), ('>=', '>='), ('<=', '<=')], help_text='Has the result to be equal, smaller, or bigger then this value.', max_length=50)),
                ('optional', models.BooleanField(default=False, help_text='Has this requirement to be fulfilled.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Consumable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The consumable name.', max_length=254, unique=True)),
                ('description', models.CharField(blank=True, help_text='Description of the consumable.', max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('part', models.FileField(help_text='The uploaded 3d part.', upload_to=core.models.model_upload_path, validators=[eopp.validations.validate_file_extension_3dpart])),
                ('is_valid', models.BooleanField(default=False, editable=False, help_text='Is the 3d part valid (a closed/watertight 3d part).')),
                ('volume', models.FloatField(blank=True, editable=False, help_text='Volume of the part.', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('bounding_box_x', models.FloatField(blank=True, editable=False, help_text='Length (x-axis) of the bounding box of the part.', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('bounding_box_y', models.FloatField(blank=True, editable=False, help_text='Width (y-axis) of the bounding box of the part.', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('bounding_box_z', models.FloatField(blank=True, editable=False, help_text='Height (z-axis) of the bounding box of the part.', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The requirement name.', max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(help_text='The category of the requirement.', on_delete=django.db.models.deletion.CASCADE, related_name='Requirement', to='core.category')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The resource name.', max_length=254, unique=True)),
                ('manufacturer', models.CharField(blank=True, help_text='Manufacturer of the resource.', max_length=254)),
                ('description', models.CharField(blank=True, help_text='Description of the resource e.g. machine type.', max_length=254)),
                ('postal_code', models.PositiveIntegerField(help_text='Postal code.', validators=[django.core.validators.MinValueValidator(0)])),
                ('street', models.CharField(help_text='Street.', max_length=254)),
                ('city', models.CharField(help_text='City.', max_length=254)),
                ('country', django_countries.fields.CountryField(help_text='Country.', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ResourceSkill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, help_text='Specific description of the resource skill (e.g. level/quality of the skill).', max_length=254)),
                ('quantity_price', models.PositiveIntegerField(default=0, help_text='The costs in € to use the skill for one unit of theskill (without consumables).', validators=[django.core.validators.MinValueValidator(0)])),
                ('quantity_time', models.PositiveIntegerField(default=0, help_text='The required time in s to apply the skill for one unit of the skill.', validators=[django.core.validators.MinValueValidator(0)])),
                ('quantity_co2', models.PositiveIntegerField(default=0, help_text='The required CO2-e to use the skill for one unit (without consumables).', validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('abilities', models.ManyToManyField(help_text='Abilities of the specific resource skill.', related_name='ResourceSkill', through='core.Ability', to='core.Requirement')),
            ],
            options={
                'ordering': ['resource'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The unit name.', max_length=254, unique=True)),
                ('description', models.CharField(blank=True, help_text='Description of the unit.', max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SkillConsumable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=0, help_text='The quantity required in the consumable unit to use the skill for one unit.', validators=[django.core.validators.MinValueValidator(0)])),
                ('quantity_price', models.PositiveIntegerField(default=0, help_text='The costs in € of the consumable to use the skill for one unit.', validators=[django.core.validators.MinValueValidator(0)])),
                ('quantity_co2', models.PositiveIntegerField(default=0, help_text='The CO2-e of the consumable to use the skill for one unit.', validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('consumable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SkillConsumable', to='core.consumable')),
                ('resource_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SkillConsumable', to='core.resourceskill')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The skill name.', max_length=254)),
                ('description', models.CharField(blank=True, help_text='Description of the skill.', max_length=254)),
                ('manufacturing_process', models.CharField(choices=[('Primary shaping', 'Primary shaping'), ('Forming', 'Forming'), ('Separation', 'Separation'), ('Joining', 'Joining'), ('Coating', 'Coating'), ('Changing material properties', 'Changing material properties')], help_text='The manufacturing process according to DIN 8580.', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unit', models.ForeignKey(help_text='Description of the skill unit (e.g. painting of 1 mm^2. Using the unit, we calculate the meta data (costs, CO2-e etc.). For example to paint 4 mm^2 the costs are 4*unit of the resource in €).', on_delete=django.db.models.deletion.CASCADE, related_name='Skill', to='core.unit')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='resourceskill',
            name='consumables',
            field=models.ManyToManyField(help_text='Consumables of the specific resource skill.', related_name='ResourceSkill', through='core.SkillConsumable', to='core.Consumable'),
        ),
        migrations.AddField(
            model_name='resourceskill',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ResourceSkill', to='core.resource'),
        ),
        migrations.AddField(
            model_name='resourceskill',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ResourceSkill', to='core.skill'),
        ),
        migrations.AddField(
            model_name='resource',
            name='skills',
            field=models.ManyToManyField(help_text='Skills of the resource.', related_name='Resource', through='core.ResourceSkill', to='core.Skill'),
        ),
        migrations.AddField(
            model_name='requirement',
            name='unit',
            field=models.ForeignKey(help_text='The unit of the Requirement.', on_delete=django.db.models.deletion.CASCADE, related_name='Requirement', to='core.unit'),
        ),
        migrations.CreateModel(
            name='ProcessStep',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('manufacturing_process', models.CharField(choices=[('Primary shaping', 'Primary shaping'), ('Forming', 'Forming'), ('Separation', 'Separation'), ('Joining', 'Joining'), ('Coating', 'Coating'), ('Changing material properties', 'Changing material properties')], help_text='The manufacturing process according to DIN 8580.', max_length=50, unique=True)),
                ('description', models.CharField(blank=True, help_text='Description of the manufacturing process.', max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unit', models.ForeignKey(help_text='The unit of the process step.', on_delete=django.db.models.deletion.CASCADE, related_name='ProcessStep', to='core.unit')),
            ],
            options={
                'ordering': ['manufacturing_process'],
            },
        ),
        migrations.CreateModel(
            name='PartManufacturingProcess',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, help_text='Description of the manufacturing step.', max_length=254)),
                ('required_quantity', models.PositiveIntegerField(default=0, help_text='The required quantity of this process step to manufacture the part.', validators=[django.core.validators.MinValueValidator(0)])),
                ('manufacturing_possibility', models.PositiveIntegerField(default=1, help_text='The number of the manufacturing possibility this process step belongs to.', validators=[django.core.validators.MinValueValidator(0)])),
                ('manufacturing_sequence_number', models.PositiveIntegerField(default=1, help_text='The number of the manufacturing sequence this process step belongs to. Starting from 1.', validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('constraints', models.ManyToManyField(help_text='Constraints of the specific part manufacturing process step.', related_name='PartManufacturingProcess', through='core.Constraint', to='core.Requirement')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PartManufacturingProcess', to='core.part')),
                ('process_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PartManufacturingProcess', to='core.processstep')),
            ],
            options={
                'verbose_name_plural': 'Part manufacturing processes',
                'ordering': ['part'],
            },
        ),
        migrations.AddField(
            model_name='part',
            name='process_steps',
            field=models.ManyToManyField(help_text='Required skills to manufacture the part.', related_name='Parts', through='core.PartManufacturingProcess', to='core.ProcessStep'),
        ),
        migrations.AddField(
            model_name='consumable',
            name='unit',
            field=models.ForeignKey(help_text='The unit of the consumable.', on_delete=django.db.models.deletion.CASCADE, related_name='Consumable', to='core.unit'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='part_manufacturing_process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Constraint', to='core.partmanufacturingprocess'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Constraint', to='core.requirement'),
        ),
        migrations.AddField(
            model_name='ability',
            name='requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Ability', to='core.requirement'),
        ),
        migrations.AddField(
            model_name='ability',
            name='resource_skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Ability', to='core.resourceskill'),
        ),
    ]
