# Generated by Django 3.1.1 on 2020-11-12 21:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20201112_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='evaluation_method',
            field=models.IntegerField(default=3, help_text='The evaluation method.\n1: Ranking regarding single field values (e.g. price).\n2: Ranking regarding normalized and weighted criteria (price, time and co2).\n 3: Ranking using the CRITIC method. The importance weights are not considered.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)]),
        ),
        migrations.AlterField(
            model_name='part',
            name='co2_importance',
            field=models.IntegerField(default=1, help_text="The importance (weight) of the co2 for the evaluation of the solutions. Only used for evaluation method '2'.", validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='part',
            name='price_importance',
            field=models.IntegerField(default=1, help_text="The importance (weight) of the price for the evaluation of the solutions. Only used for evaluation method '2'.", validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='part',
            name='time_importance',
            field=models.IntegerField(default=1, help_text="The importance (weight) of the time for the evaluation of the solutions. Only used for evaluation method '2'.", validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
