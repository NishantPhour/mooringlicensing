# Generated by Django 5.0.9 on 2025-01-08 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0385_alter_numberofdaystype_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationfee',
            name='payment_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='dcvadmissionfee',
            name='payment_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='dcvpermitfee',
            name='payment_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='stickeractionfee',
            name='payment_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]