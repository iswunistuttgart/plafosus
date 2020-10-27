# Generated by Django 3.1.1 on 2020-10-26 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processstep',
            name='manufacturing_process',
            field=models.CharField(choices=[('Primary shaping', 'Primary shaping'), ('Forming', 'Forming'), ('Separation', 'Separation'), ('Joining', 'Joining'), ('Coating', 'Coating'), ('Changing material properties', 'Changing material properties')], help_text='The manufacturing process according to DIN 8580.', max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='processstep',
            unique_together={('manufacturing_process', 'unit')},
        ),
    ]
