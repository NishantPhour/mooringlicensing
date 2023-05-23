# Generated by Django 3.2.18 on 2023-05-17 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0308_auto_20230516_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vesselownership',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mooringlicensing.owner'),
        ),
        migrations.AlterField(
            model_name='vesselownership',
            name='vessel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mooringlicensing.vessel'),
        ),
    ]
