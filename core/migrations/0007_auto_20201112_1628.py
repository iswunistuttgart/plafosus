# Generated by Django 3.1.1 on 2020-11-12 15:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20201112_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skillconsumable',
            old_name='quantity_co2',
            new_name='variable_co2',
        ),
        migrations.RenameField(
            model_name='skillconsumable',
            old_name='quantity_price',
            new_name='variable_price',
        ),
        migrations.RemoveField(
            model_name='skillconsumable',
            name='quantity_time',
        ),
        migrations.AddField(
            model_name='resourceskill',
            name='variable_co2',
            field=models.PositiveIntegerField(default=0, help_text='The variable CO2-e to use the skill.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='resourceskill',
            name='variable_price',
            field=models.PositiveIntegerField(default=0, help_text='The variable costs in € to use the skill.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='resourceskill',
            name='variable_time',
            field=models.PositiveIntegerField(default=0, help_text='The variable time in s to use the skill.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
