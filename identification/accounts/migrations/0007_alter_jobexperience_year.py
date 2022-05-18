# Generated by Django 4.0 on 2022-05-17 21:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_jobexperience_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobexperience',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(2022), django.core.validators.MinValueValidator(1950)]),
        ),
    ]