# Generated by Django 5.0.6 on 2024-06-28 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_dayofweek_scheduleversion_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayofweek',
            name='language',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.language'),
            preserve_default=False,
        ),
    ]