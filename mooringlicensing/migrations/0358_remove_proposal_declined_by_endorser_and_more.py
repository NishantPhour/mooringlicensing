# Generated by Django 5.0.9 on 2024-09-17 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0357_proposalsitelicenseemooringrequest_approved_by_endorser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='declined_by_endorser',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='endorser_reminder_sent',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='mooring',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='site_licensee_email',
        ),
    ]
