# Generated by Django 3.2.20 on 2023-10-13 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0333_auto_20231010_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='declined_by_endorser',
            field=models.BooleanField(default=False),
        ),
    ]
