# Generated by Django 3.1.1 on 2021-04-22 14:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skillconsumable',
            name='fixed_co2',
        ),
        migrations.RemoveField(
            model_name='skillconsumable',
            name='fixed_price',
        ),
        migrations.RemoveField(
            model_name='skillconsumable',
            name='variable_co2',
        ),
        migrations.RemoveField(
            model_name='skillconsumable',
            name='variable_price',
        ),
        migrations.AddField(
            model_name='skillconsumable',
            name='co2',
            field=models.FloatField(default=0, help_text='The CO2-eq. for one unit of this consumable.'),
        ),
        migrations.AddField(
            model_name='skillconsumable',
            name='price',
            field=models.FloatField(default=0, help_text='The costs in € for one unit of this consumable (e.g. 0.29 € for 1 kWh).'),
        ),
        migrations.AlterField(
            model_name='part',
            name='co2_importance',
            field=models.IntegerField(default=1, help_text="The importance (weight) of the CO2-eq. for the evaluation of the solutions. Only used for evaluation method '2'.", validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='part',
            name='evaluation_method',
            field=models.IntegerField(default=3, help_text='The evaluation method. 1: Ranking regarding single field values (e.g. price). The highest importance weight is considered first. 2: Ranking regarding normalized and weighted criteria (price, time and CO2-eq.). 3: Ranking using the CRITIC method. The importance weights are not considered.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)]),
        ),
        migrations.AlterField(
            model_name='processstep',
            name='manufacturing_process',
            field=models.CharField(help_text='The manufacturing process.', max_length=50),
        ),
        migrations.AlterField(
            model_name='resourceskill',
            name='fixed_co2',
            field=models.FloatField(default=0, help_text='The fixed CO2-eq. to use the skill.'),
        ),
        migrations.AlterField(
            model_name='resourceskill',
            name='variable_co2',
            field=models.FloatField(default=0, help_text='The variable CO2-eq. to use the skill per its unit.'),
        ),
        migrations.AlterField(
            model_name='resourceskill',
            name='variable_price',
            field=models.FloatField(default=0, help_text='The variable costs in € to use the skill per its unit.'),
        ),
        migrations.AlterField(
            model_name='resourceskill',
            name='variable_time',
            field=models.FloatField(default=0, help_text='The variable time in s to use the skill per its unit.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='skillconsumable',
            name='fixed_quantity',
            field=models.FloatField(default=0, help_text='The quantity required in the consumable unit to use the skill once (e.g. warm-up phase).', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='skillconsumable',
            name='variable_quantity',
            field=models.FloatField(default=0, help_text='The quantity required in the consumable unit to use one unit of the skill (e.g. 1 mm³ milling requires 0.2 kWh).', validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
