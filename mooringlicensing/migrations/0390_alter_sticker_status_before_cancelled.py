# Generated by Django 5.0.11 on 2025-01-16 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0389_mooringonapproval_previous_sticker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sticker',
            name='status_before_cancelled',
            field=models.CharField(blank=True, choices=[('ready', 'Ready'), ('not_ready_yet', 'Not Ready Yet'), ('awaiting_printing', 'Awaiting Printing'), ('current', 'Current'), ('to_be_returned', 'To be Returned'), ('returned', 'Returned'), ('lost', 'Lost'), ('expired', 'Expired'), ('cancelled', 'Cancelled')], max_length=40, null=True),
        ),
    ]
