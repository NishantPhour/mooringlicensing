# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-03-26 02:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mooringlicensing', '0028_auto_20210324_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_invoice', models.BooleanField(default=False)),
                ('confirmation_sent', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expiry_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('payment_type', models.SmallIntegerField(choices=[(0, 'Internet booking'), (1, 'Reception booking'), (2, 'Black booking'), (3, 'Temporary reservation')], default=0)),
                ('cost', models.DecimalField(decimal_places=2, default='0.00', max_digits=8)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_by_application_fee', to=settings.AUTH_USER_MODEL)),
                ('proposal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='application_fees', to='mooringlicensing.Proposal')),
            ],
        ),
    ]