# Generated by Django 5.0.6 on 2024-06-24 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_studentoffaculty_is_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentoffaculty',
            name='is_current',
            field=models.BooleanField(),
        ),
    ]
