# Generated by Django 5.0.9 on 2025-01-06 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0383_alter_proposaltype_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissiontype',
            name='code',
            field=models.CharField(choices=[('landing', 'Landing'), ('extended_stay', 'Extended stay'), ('water_based', 'Water based'), ('approved_events', 'Approved events')], default='landing', max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='agegroup',
            name='code',
            field=models.CharField(choices=[('adult', 'Adult'), ('child', 'Child')], default='adult', max_length=40, unique=True),
        ),
    ]