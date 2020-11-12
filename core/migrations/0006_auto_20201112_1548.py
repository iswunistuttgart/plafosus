# Generated by Django 3.1.1 on 2020-11-12 14:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20201028_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resourceskill',
            name='quantity_co2',
        ),
        migrations.RemoveField(
            model_name='resourceskill',
            name='quantity_price',
        ),
        migrations.RemoveField(
            model_name='resourceskill',
            name='quantity_time',
        ),
        migrations.AddField(
            model_name='resourceskill',
            name='fixed_co2',
            field=models.PositiveIntegerField(default=0, help_text='The fixed CO2-e to use the skill.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='resourceskill',
            name='fixed_price',
            field=models.PositiveIntegerField(default=0, help_text='The fixed costs in € to use the skill.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='resourceskill',
            name='fixed_time',
            field=models.PositiveIntegerField(default=0, help_text='The fixed time in s to use the skill (e.g. initial machine preparation).', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='skillconsumable',
            name='quantity_time',
            field=models.PositiveIntegerField(default=0, help_text='The required time in s for one unit of this consumable.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
