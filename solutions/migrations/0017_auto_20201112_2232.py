# Generated by Django 3.1.1 on 2020-11-12 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0016_auto_20201112_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permutation',
            name='comparison_value',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='The comparison value of this permutation.', max_digits=5, null=True),
        ),
    ]
