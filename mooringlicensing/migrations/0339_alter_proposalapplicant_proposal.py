# Generated by Django 5.0.8 on 2024-08-13 07:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0338_delete_usersystemsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalapplicant',
            name='proposal',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mooringlicensing.proposal'),
        ),
    ]