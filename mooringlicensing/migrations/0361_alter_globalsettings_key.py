# Generated by Django 5.0.9 on 2024-09-25 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0360_remove_compliance_reminder_sent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalsettings',
            name='key',
            field=models.CharField(choices=[('dcv_permit_template_file', 'DcvPermit template file'), ('dcv_admission_template_file', 'DcvAdmission template file'), ('wla_template_file', 'Waiting List Allocation template file'), ('aap_template_file', 'Annual Admission Permit template file'), ('aup_template_file', 'Authorised User Permit template file'), ('ml_template_file', 'Mooring Site Licence template file'), ('ml_au_list_template_file', 'Mooring Site Licence Authorised User Summary template file'), ('minimum_vessel_length', 'Minimum vessel length'), ('minimum_mooring_vessel_length', 'Minimum mooring vessel length'), ('external_dashboard_sections_list', 'External dashboard sections list'), ('number_of_moorings_to_return_for_lookup', 'Number of moorings to return for lookup'), ('fee_amount_of_swap_moorings', 'Fee amount of swap moorings'), ('swap_moorings_includes_gst', 'Fee for swap moorings includes gst')], max_length=255),
        ),
    ]
