# Generated by Django 5.0.8 on 2024-08-14 07:35

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0338_delete_usersystemsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalapplicant',
            name='first_name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Given name(s)'),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='last_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='postal_country',
            field=django_countries.fields.CountryField(blank=True, default='AU', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='postal_line1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Line 1'),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='postal_line2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Line 2'),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='postal_line3',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Line 3'),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='postal_postcode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='postal_state',
            field=models.CharField(blank=True, default='WA', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='residential_country',
            field=django_countries.fields.CountryField(blank=True, default='AU', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='residential_line1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Line 1'),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='residential_line2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Line 2'),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='residential_line3',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Line 3'),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='residential_locality',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Suburb / Town'),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='residential_postcode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='residential_state',
            field=models.CharField(blank=True, default='WA', max_length=255, null=True),
        ),
    ]
