# Generated by Django 3.2.23 on 2024-03-07 01:53

import django.core.files.storage
from django.db import migrations, models
import mooringlicensing.components.proposals.models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0335_applicationfee_handled_in_preload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalsettings',
            name='key',
            field=models.CharField(choices=[('dcv_permit_template_file', 'DcvPermit template file'), ('dcv_admission_template_file', 'DcvAdmission template file'), ('wla_template_file', 'Waiting List Allocation template file'), ('aap_template_file', 'Annual Admission Permit template file'), ('aup_template_file', 'Authorised User Permit template file'), ('ml_template_file', 'Mooring Site Licence template file'), ('ml_au_list_template_file', 'Mooring Site Licence Authorised User Summary template file'), ('minimum_vessel_length', 'Minimum vessel length'), ('minimum_mooring_vessel_length', 'Minimum mooring vessel length'), ('min_sticker_number_for_dcv_permit', 'Minimun sticker number for DCV Permit'), ('external_dashboard_sections_list', 'External dashboard sections list'), ('number_of_moorings_to_return_for_lookup', 'Number of moorings to return for lookup'), ('fee_amount_of_swap_moorings', 'Fee amount of swap moorings'), ('swap_moorings_includes_gst', 'Fee for swap moorings includes gst')], max_length=255),
        ),
        migrations.AlterField(
            model_name='hullidentificationnumberdocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.HullIdentificationNumberDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='vesselregistrationdocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.VesselRegistrationDocument.upload_to),
        ),
    ]
