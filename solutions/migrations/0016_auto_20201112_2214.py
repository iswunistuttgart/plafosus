# Generated by Django 3.1.1 on 2020-11-12 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0015_remove_consumablecost_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permutation',
            name='comparison_value',
            field=models.FloatField(blank=True, help_text='The comparison value of this permutation.', null=True),
        ),
    ]
