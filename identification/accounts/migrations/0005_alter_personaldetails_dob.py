# Generated by Django 4.0 on 2022-05-20 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_jobexperience_year_alter_qualification_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldetails',
            name='dob',
            field=models.DateField(null=True),
        ),
    ]