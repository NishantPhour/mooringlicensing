# Generated by Django 3.2.20 on 2023-08-22 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0317_delete_backtoassessor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissiontype',
            name='code',
            field=models.CharField(choices=[('landing', 'Landing'), ('extended_stay', 'Extended stay'), ('water_based', 'Water based'), ('approved_events', 'Approved events')], default='landing', max_length=40),
        ),
    ]
