# Generated by Django 5.0.9 on 2025-01-06 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0384_alter_admissiontype_code_alter_agegroup_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberofdaystype',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
