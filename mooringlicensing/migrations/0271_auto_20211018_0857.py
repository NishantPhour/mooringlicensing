# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-10-18 00:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mooringlicensing.components.approvals.models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0270_auto_20211015_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorisedUserSummaryDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('_file', models.FileField(max_length=512, upload_to=mooringlicensing.components.approvals.models.update_approval_doc_filename)),
                ('approval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorised_user_summary_documents', to='mooringlicensing.Approval')),
            ],
        ),
        migrations.AddField(
            model_name='approval',
            name='authorised_user_summary_document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approvals', to='mooringlicensing.AuthorisedUserSummaryDocument'),
        ),
    ]
