# Generated by Django 3.2.18 on 2023-03-22 03:29

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0301_auto_20230320_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalapplicant',
            name='residential_country',
            field=django_countries.fields.CountryField(blank=True, default='AU', max_length=2),
        ),
        migrations.AddField(
            model_name='proposalapplicant',
            name='residential_line1',
            field=models.CharField(blank=True, max_length=255, verbose_name='Line 1'),
        ),
        migrations.AddField(
            model_name='proposalapplicant',
            name='residential_line2',
            field=models.CharField(blank=True, max_length=255, verbose_name='Line 2'),
        ),
        migrations.AddField(
            model_name='proposalapplicant',
            name='residential_line3',
            field=models.CharField(blank=True, max_length=255, verbose_name='Line 3'),
        ),
        migrations.AddField(
            model_name='proposalapplicant',
            name='residential_locality',
            field=models.CharField(blank=True, max_length=255, verbose_name='Suburb / Town'),
        ),
        migrations.AddField(
            model_name='proposalapplicant',
            name='residential_postcode',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='proposalapplicant',
            name='residential_state',
            field=models.CharField(blank=True, default='WA', max_length=255),
        ),
    ]