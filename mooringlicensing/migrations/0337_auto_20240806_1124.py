# Generated by Django 3.2.23 on 2024-08-06 03:24

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import mooringlicensing.components.approvals.models
import mooringlicensing.components.compliances.models
#import mooringlicensing.components.organisations.models
import mooringlicensing.components.proposals.models
import mooringlicensing.components.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('mooringlicensing', '0336_auto_20240307_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approval',
            name='extracted_fields',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='approval',
            name='surrender_details',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='approval',
            name='suspension_details',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='approvaldocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.approvals.models.ApprovalDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='approvaldocument',
            name='approval',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_documents', to='mooringlicensing.approval'),
        ),
        migrations.AlterField(
            model_name='approvallogdocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.approvals.models.ApprovalLogDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='authorisedusersummarydocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.approvals.models.AuthorisedUserSummaryDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='compliancedocument',
            name='_file',
            field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.compliances.models.update_proposal_complaince_filename),
        ),
        migrations.AlterField(
            model_name='compliancelogdocument',
            name='_file',
            field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.compliances.models.update_compliance_comms_log_filename),
        ),
        migrations.AlterField(
            model_name='dcvadmissiondocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.approvals.models.DcvAdmissionDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='dcvadmissiondocument',
            name='dcv_admission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dcv_admission_documents', to='mooringlicensing.dcvadmission'),
        ),
        migrations.AlterField(
            model_name='dcvpermitdocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.approvals.models.DcvPermitDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='dcvpermitdocument',
            name='dcv_permit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dcv_permit_documents', to='mooringlicensing.dcvpermit'),
        ),
        migrations.AlterField(
            model_name='electoralrolldocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.ElectoralRollDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='emailuserlogdocument',
            name='_file',
            field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.users.models.update_emailuser_comms_log_filename),
        ),
        migrations.AlterField(
            model_name='insurancecertificatedocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.InsuranceCertificateDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='mooringlogdocument',
            name='_file',
            field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.update_mooring_comms_log_filename),
        ),
        migrations.AlterField(
            model_name='mooringreportdocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.MooringReportDocument.upload_to),
        ),
        #migrations.AlterField(
        #    model_name='organisationlogdocument',
        #    name='_file',
        #    field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.organisations.models.update_organisation_comms_log_filename),
        #),
        migrations.AlterField(
            model_name='organisationrequest',
            name='identification',
            field=models.FileField(blank=True, max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to='organisation/requests/%Y/%m/%d'),
        ),
        #migrations.AlterField(
        #    model_name='organisationrequestlogdocument',
        #    name='_file',
        #    field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.organisations.models.update_organisation_request_comms_log_filename),
        #),
        migrations.AlterField(
            model_name='proofofidentitydocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.ProofOfIdentityDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='assessor_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='comment_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='individual_owner',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='proposed_issuance_approval',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='silent_elector',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='proposalapplicant',
            name='postal_same_as_residential',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='proposaldocument',
            name='_file',
            field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.update_proposal_doc_filename),
        ),
        migrations.AlterField(
            model_name='proposallogdocument',
            name='_file',
            field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.update_proposal_comms_log_filename),
        ),
        migrations.AlterField(
            model_name='renewaldocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.approvals.models.RenewalDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='requirementdocument',
            name='_file',
            field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.update_requirement_doc_filename),
        ),
        migrations.AlterField(
            model_name='signedlicenceagreementdocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.SignedLicenceAgreementDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='stickerprintingbatch',
            name='_file',
            field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.update_sticker_doc_filename),
        ),
        migrations.AlterField(
            model_name='stickerprintingresponse',
            name='_file',
            field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.update_sticker_response_doc_filename),
        ),
        migrations.AlterField(
            model_name='stickerprintingresponse',
            name='no_errors_when_process',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='temporarydocument',
            name='_file',
            field=models.FileField(max_length=255, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='vessellogdocument',
            name='_file',
            field=models.FileField(max_length=512, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.update_vessel_comms_log_filename),
        ),
        migrations.AlterField(
            model_name='vesselownership',
            name='company_ownerships',
            field=models.ManyToManyField(blank=True, related_name='vessel_ownerships', through='mooringlicensing.VesselOwnershipCompanyOwnership', to='mooringlicensing.CompanyOwnership'),
        ),
        migrations.AlterField(
            model_name='waitinglistofferdocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.approvals.models.WaitingListOfferDocument.upload_to),
        ),
        migrations.AlterField(
            model_name='writtenproofdocument',
            name='_file',
            field=models.FileField(max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/mooringlicensing/private-media'), upload_to=mooringlicensing.components.proposals.models.WrittenProofDocument.upload_to),
        ),
    ]
