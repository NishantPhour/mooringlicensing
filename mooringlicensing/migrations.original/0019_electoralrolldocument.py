# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-03-22 08:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mooringlicensing.components.main.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mooringlicensing', '0018_vesseldetails_vessel_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectoralRollDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('_file', models.FileField(max_length=512, upload_to=mooringlicensing.components.main.models.update_electoral_roll_doc_filename)),
                ('input_name', models.CharField(blank=True, max_length=255, null=True)),
                ('can_delete', models.BooleanField(default=True)),
                ('can_hide', models.BooleanField(default=False)),
                ('hidden', models.BooleanField(default=False)),
                ('emailuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='electoralroll_documents', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Electoral Roll Document',
            },
        ),
    ]