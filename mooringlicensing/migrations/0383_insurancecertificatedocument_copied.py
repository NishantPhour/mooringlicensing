# Generated by Django 5.0.9 on 2025-01-17 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0382_sticker_invoice_property_cache'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurancecertificatedocument',
            name='copied',
            field=models.BooleanField(default=False),
        ),
    ]
