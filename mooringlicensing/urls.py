from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from django_media_serv.urls import urlpatterns as media_serv_patterns

import mooringlicensing
# import mooringlicensing.components.approvals.api
from mooringlicensing import views
from mooringlicensing.components.approvals.views import DcvAdmissionFormView
from mooringlicensing.components.main.utils import update_personal_details
from mooringlicensing.components.payments_ml.views import ApplicationFeeView, ApplicationFeeSuccessView, InvoicePDFView, \
    DcvPermitFeeView, DcvPermitFeeSuccessView, DcvPermitPDFView, ConfirmationView, DcvAdmissionFeeView, \
    DcvAdmissionFeeSuccessView, DcvAdmissionPDFView, ApplicationFeeExistingView, StickerReplacementFeeView, \
    StickerReplacementFeeSuccessView, RefundProposalHistoryView, ProposalPaymentHistoryView, ApplicationFeeAlreadyPaid, \
    ApplicationFeeSuccessViewPreload, DcvPermitFeeSuccessViewPreload, DcvAdmissionFeeSuccessViewPreload, \
    StickerReplacementFeeSuccessViewPreload
from mooringlicensing.components.proposals import views as proposal_views
from mooringlicensing.components.organisations import views as organisation_views
from mooringlicensing.components.payments_ml import api as payments_api
from mooringlicensing.components.proposals import api as proposal_api
from mooringlicensing.components.approvals import api as approval_api
from mooringlicensing.components.compliances import api as compliances_api
from mooringlicensing.components.proposals.views import AuthorisedUserApplicationEndorseView, \
    MooringLicenceApplicationDocumentsUploadView
from mooringlicensing.components.users import api as users_api
from mooringlicensing.components.organisations import api as org_api
from mooringlicensing.components.main import api as main_api
# from ledger.urls import urlpatterns as ledger_patterns
from ledger_api_client.urls import urlpatterns as ledger_patterns

# API patterns
from mooringlicensing.management.default_data_manager import DefaultDataManager
from mooringlicensing.settings import PRIVATE_MEDIA_DIR_NAME
from mooringlicensing.utils import are_migrations_running
from django.urls import path

router = routers.DefaultRouter()
if settings.DEBUG is not True:
    router.include_root_view = False
router.register(r'organisations', org_api.OrganisationViewSet)
router.register(r'proposal', proposal_api.ProposalViewSet)
router.register(r'proposal_by_uuid', proposal_api.ProposalByUuidViewSet)
router.register(r'waitinglistapplication', proposal_api.WaitingListApplicationViewSet)
router.register(r'annualadmissionapplication', proposal_api.AnnualAdmissionApplicationViewSet)
router.register(r'authoriseduserapplication', proposal_api.AuthorisedUserApplicationViewSet)
router.register(r'mooringlicenceapplication', proposal_api.MooringLicenceApplicationViewSet)
router.register(r'proposals_paginated', proposal_api.ProposalPaginatedViewSet)
router.register(r'approvals_paginated', approval_api.ApprovalPaginatedViewSet)
router.register(r'dcvpermits_paginated', approval_api.DcvPermitPaginatedViewSet)
router.register(r'dcvadmissions_paginated', approval_api.DcvAdmissionPaginatedViewSet)
router.register(r'stickers_paginated', approval_api.StickerPaginatedViewSet)
router.register(r'stickers', approval_api.StickerViewSet)
router.register(r'compliances_paginated', compliances_api.CompliancePaginatedViewSet)
router.register(r'moorings_paginated', proposal_api.MooringPaginatedViewSet)
router.register(r'approvals', approval_api.ApprovalViewSet)
router.register(r'waitinglistallocation', approval_api.WaitingListAllocationViewSet)
# router.register(r'mooringlicence', approval_api.MooringLicenceViewSet)
router.register(r'compliances', compliances_api.ComplianceViewSet)
router.register(r'proposal_requirements', proposal_api.ProposalRequirementViewSet)
router.register(r'proposal_standard_requirements', proposal_api.ProposalStandardRequirementViewSet)
router.register(r'organisation_requests', org_api.OrganisationRequestsViewSet)
router.register(r'organisation_contacts', org_api.OrganisationContactViewSet)
router.register(r'my_organisations', org_api.MyOrganisationsViewSet)
router.register(r'users', users_api.UserViewSet)
router.register(r'amendment_request', proposal_api.AmendmentRequestViewSet)
# router.register(r'back_to_assessor', proposal_api.BackToAssessorViewSet)
router.register(r'compliance_amendment_request', compliances_api.ComplianceAmendmentRequestViewSet)
# router.register(r'global_settings', main_api.GlobalSettingsViewSet)
router.register(r'payment', main_api.PaymentViewSet)
router.register(r'mooringbays', proposal_api.MooringBayViewSet)
router.register(r'vessel', proposal_api.VesselViewSet)
router.register(r'mooring', proposal_api.MooringViewSet)
router.register(r'dcv_vessel', approval_api.DcvVesselViewSet)
router.register(r'vesselownership', proposal_api.VesselOwnershipViewSet)
router.register(r'dcv_permit', mooringlicensing.components.approvals.api.DcvPermitViewSet)
router.register(r'dcv_admission', mooringlicensing.components.approvals.api.DcvAdmissionViewSet)
router.register(r'company', proposal_api.CompanyViewSet)
router.register(r'companyownership', proposal_api.CompanyOwnershipViewSet)
router.register(r'temporary_document', main_api.TemporaryDocumentCollectionViewSet)

api_patterns = [
    url(r'^api/profile$', users_api.GetProfile.as_view(), name='get-profile'),
    url(r'^api/profile/(?P<proposal_pk>\d+)$', users_api.GetProposalApplicant.as_view(), name='get-proposal-applicant'),


    url(r'^api/countries$', users_api.GetCountries.as_view(), name='get-countries'),
    url(r'^api/submitter_profile$', users_api.GetSubmitterProfile.as_view(), name='get-submitter-profile'),
    url(r'^api/filtered_users$', users_api.UserListFilterView.as_view(), name='filtered_users'),
    url(r'^api/filtered_organisations$', org_api.OrganisationListFilterView.as_view(), name='filtered_organisations'),
    url(r'^api/filtered_payments$', approval_api.ApprovalPaymentFilterViewSet.as_view(), name='filtered_payments'),
    url(r'^api/application_types$', proposal_api.GetApplicationTypeDescriptions.as_view(), name='get-application-type-descriptions'),
    url(r'^api/application_types_dict$', proposal_api.GetApplicationTypeDict.as_view(), name='get-application-type-dict'),
    url(r'^api/application_categories_dict$', proposal_api.GetApplicationCategoryDict.as_view(), name='get-application-category-dict'),
    # url(r'^api/applicants_dict$', proposal_api.GetApplicantsDict.as_view(), name='get-applicants-dict'),
    url(r'^api/payment_system_id$', proposal_api.GetPaymentSystemId.as_view(), name='get-payment-system-id'),
    url(r'^api/fee_item_sticker_replacement$', proposal_api.GetStickerReplacementFeeItem.as_view(), name='get-sticker-replacement-fee-item'),
    url(r'^api/vessel_rego_nos$', proposal_api.GetVesselRegoNos.as_view(), name='get-vessel_rego-nos'),
    url(r'^api/mooring_lookup$', proposal_api.GetMooring.as_view(), name='get-mooring'),
    url(r'^api/mooring_lookup_per_bay$', proposal_api.GetMooringPerBay.as_view(), name='get-mooring-per-bay'),
    url(r'^api/vessel_lookup$', proposal_api.GetVessel.as_view(), name='get-vessel'),
    url(r'^api/sticker_lookup$', approval_api.GetSticker.as_view(), name='get-sticker'),
    url(r'^api/person_lookup$', users_api.GetPerson.as_view(), name='get-person'),
    url(r'^api/company_names$', proposal_api.GetCompanyNames.as_view(), name='get-company-names'),
    url(r'^api/dcv_vessel_rego_nos$', proposal_api.GetDcvVesselRegoNos.as_view(), name='get-dcv-vessel_rego-nos'),
    url(r'^api/dcv_organisations$', proposal_api.GetDcvOrganisations.as_view(), name='get-dcv-organisations'),
    url(r'^api/fee_configurations$', payments_api.GetFeeConfigurations.as_view(), name='get-fee-configurations'),
    url(r'^api/vessel_types_dict$', proposal_api.GetVesselTypesDict.as_view(), name='get-vessel-types-dict'),
    url(r'^api/insurance_choices_dict$', proposal_api.GetInsuranceChoicesDict.as_view(), name='get-insurance-choices-dict'),
    url(r'^api/application_statuses_dict$', proposal_api.GetApplicationStatusesDict.as_view(), name='get-application-statuses-dict'),
    url(r'^api/approval_types_dict$', approval_api.GetApprovalTypeDict.as_view(), name='get-approval-type-dict'),
    url(r'^api/wla_allowed$', approval_api.GetWlaAllowed.as_view(), name='get-wla-allowed'),
    url(r'^api/current_season$', approval_api.GetCurrentSeason.as_view(), name='get-current-season'),
    url(r'^api/approval_statuses_dict$', approval_api.GetApprovalStatusesDict.as_view(), name='get-approval-statuses-dict'),
    url(r'^api/fee_seasons_dict$', approval_api.GetFeeSeasonsDict.as_view(), name='get-fee-seasons-dict'),
    url(r'^api/sticker_status_dict$', approval_api.GetStickerStatusDict.as_view(), name='get-sticker-status-dict'),
    url(r'^api/daily_admission_url$', approval_api.GetDailyAdmissionUrl.as_view(), name='get-daily-admission-url'),
    url(r'^api/seasons_for_dcv_dict$', payments_api.GetSeasonsForDcvPermitDict.as_view(), name='get-approval-statuses-dict'),
    url(r'^api/compliance_statuses_dict$', compliances_api.GetComplianceStatusesDict.as_view(), name='get-compliance-statuses-dict'),
    url(r'^api/mooring_statuses_dict$', proposal_api.GetMooringStatusesDict.as_view(), name='get-mooring-statuses-dict'),
    url(r'^api/empty_list$', proposal_api.GetEmptyList.as_view(), name='get-empty-list'),
    url(r'^api/organisation_access_group_members',org_api.OrganisationAccessGroupMembers.as_view(),name='organisation-access-group-members'),
    url(r'^api/',include(router.urls)),
    url(r'^api/amendment_request_reason_choices',proposal_api.AmendmentRequestReasonChoicesView.as_view(),name='amendment_request_reason_choices'),
    url(r'^api/compliance_amendment_reason_choices',compliances_api.ComplianceAmendmentReasonChoicesView.as_view(),name='amendment_request_reason_choices'),
    url(r'^api/search_keywords',proposal_api.SearchKeywordsView.as_view(),name='search_keywords'),
    url(r'^api/search_reference',proposal_api.SearchReferenceView.as_view(),name='search_reference'),
    url(r'^api/oracle_job$',main_api.OracleJob.as_view(), name='get-oracle'),
    url(r'^api/reports/booking_settlements$', main_api.BookingSettlementReportView.as_view(),name='booking-settlements-report'),
    url(r'^api/external_dashboard_sections_list/$',main_api.GetExternalDashboardSectionsList.as_view(), name='get-external-dashboard-sections-list'),
]

# URL Patterns
urlpatterns = [
    # url(r'^ledger/admin/', admin.site.urls, name='ledger_admin'),
    path(r"admin/", admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'', include(api_patterns)),
    # url(r'^$', views.MooringLicensingRoutingView.as_view(), name='ds_home'),
    url(r'^$', views.MooringLicensingRoutingView.as_view(), name='home'),
    url(r'^contact/', views.MooringLicensingContactView.as_view(), name='ds_contact'),
    url(r'^further_info/', views.MooringLicensingFurtherInformationView.as_view(), name='ds_further_info'),
    url(r'^internal/', views.InternalView.as_view(), name='internal'),
    url(r'^external/', views.ExternalView.as_view(), name='external'),
    url(r'^firsttime/$', views.first_time, name='first_time'),
    url(r'^account/$', views.ExternalView.as_view(), name='manage-account'),
    url(r'^profiles/', views.ExternalView.as_view(), name='manage-profiles'),
    url(r'^help/(?P<application_type>[^/]+)/(?P<help_type>[^/]+)/$', views.HelpView.as_view(), name='help'),
    url(r'^mgt-commands/$', views.ManagementCommandsView.as_view(), name='mgt-commands'),
    url(r'^login-success/$', views.LoginSuccess.as_view(), name='login-success'),

    #following url is used to include url path when sending Proposal amendment request to user.
    url(r'^proposal/$', proposal_views.ProposalView.as_view(), name='proposal'),
    url(r'^preview/licence-pdf/(?P<proposal_pk>\d+)',proposal_views.PreviewLicencePDFView.as_view(), name='preview_licence_pdf'),

    # payment related urls
    url(r'^application_fee/(?P<proposal_pk>\d+)/$', ApplicationFeeView.as_view(), name='application_fee'),
    url(r'^application_fee_existing/(?P<invoice_reference>\d+)/$', ApplicationFeeExistingView.as_view(), name='application_fee_existing'),
    url(r'^application_fee_already_paid/(?P<proposal_pk>\d+)/$', ApplicationFeeAlreadyPaid.as_view(), name='application_fee_already_paid'),
    # url(r'^application_fee_already_paid/$', ApplicationFeeAlreadyPaid.as_view(), name='application_fee_already_paid'),
    url(r'^confirmation/(?P<proposal_pk>\d+)/$', ConfirmationView.as_view(), name='confirmation'),
    url(r'^success/fee/(?P<uuid>.+)/$', ApplicationFeeSuccessView.as_view(), name='fee_success'),
    # url(r'^success2/fee/$', ApplicationFeeSuccessViewPreload.as_view(), name='fee_success_preload'),
    url(r"ledger-api-success-callback/(?P<uuid>.+)/", ApplicationFeeSuccessViewPreload.as_view(), name="ledger-api-success-callback",),
    url(r'^dcv_permit_fee/(?P<dcv_permit_pk>\d+)/$', DcvPermitFeeView.as_view(), name='dcv_permit_fee'),
    url(r'^dcv_permit_success/(?P<uuid>.+)/$', DcvPermitFeeSuccessView.as_view(), name='dcv_permit_fee_success'),
    url(r'^dcv_permit_success_preload/(?P<uuid>.+)/$', DcvPermitFeeSuccessViewPreload.as_view(), name='dcv_permit_fee_success_preload'),
    url(r'^dcv_admission_fee/(?P<dcv_admission_pk>\d+)/$', DcvAdmissionFeeView.as_view(), name='dcv_admission_fee'),
    url(r'^dcv_admission_success/(?P<uuid>.+)/$', DcvAdmissionFeeSuccessView.as_view(), name='dcv_admission_fee_success'),
    url(r'^dcv_admission_success_preload/(?P<uuid>.+)/$', DcvAdmissionFeeSuccessViewPreload.as_view(), name='dcv_admission_fee_success_preload'),
    url(r'^sticker_replacement_fee/$', StickerReplacementFeeView.as_view(), name='sticker_replacement_fee'),
    url(r'^sticker_replacement_fee_success/(?P<uuid>.+)/$', StickerReplacementFeeSuccessView.as_view(), name='sticker_replacement_fee_success'),
    url(r'^sticker_replacement_fee_success_preload/(?P<uuid>.+)/$', StickerReplacementFeeSuccessViewPreload.as_view(), name='sticker_replacement_fee_success_preload'),
    url(r'^aua_for_endorsement/(?P<uuid_str>[a-zA-Z0-9-]+)/view/$', AuthorisedUserApplicationEndorseView.as_view(), {'action': 'view'}, name='view-url'),
    url(r'^aua_for_endorsement/(?P<uuid_str>[a-zA-Z0-9-]+)/endorse/$', AuthorisedUserApplicationEndorseView.as_view(), {'action': 'endorse'}, name='endorse-url'),
    url(r'^aua_for_endorsement/(?P<uuid_str>[a-zA-Z0-9-]+)/decline/$', AuthorisedUserApplicationEndorseView.as_view(), {'action': 'decline'}, name='decline-url'),
    url(r'^mla_documents_upload/(?P<uuid_str>[a-zA-Z0-9-]+)/$', MooringLicenceApplicationDocumentsUploadView.as_view(), name='mla-documents-upload'),
    url(r'^dcv_admission_form/$', DcvAdmissionFormView.as_view(), name='dcv_admission_form'),
    url(r'payments/invoice-pdf/(?P<reference>\d+)', InvoicePDFView.as_view(), name='invoice-pdf'),
    url(r'payments/dcv-permit-pdf/(?P<id>\d+)', DcvPermitPDFView.as_view(), name='dcv-permit-pdf'),
    url(r'payments/dcv-admission-pdf/(?P<id>\d+)', DcvAdmissionPDFView.as_view(), name='dcv-admission-pdf'),

    #following url is defined so that to include url path when sending Proposal amendment request to user.
    url(r'^external/proposal/(?P<proposal_pk>\d+)/$', views.ExternalProposalView.as_view(), name='external-proposal-detail'),
    url(r'^internal/proposal/(?P<proposal_pk>\d+)/$', views.InternalProposalView.as_view(), name='internal-proposal-detail'),
    url(r'^external/compliance/(?P<compliance_pk>\d+)/$', views.ExternalComplianceView.as_view(), name='external-compliance-detail'),
    url(r'^internal/compliance/(?P<compliance_pk>\d+)/$', views.InternalComplianceView.as_view(), name='internal-compliance-detail'),

    # reversion history-compare
    url(r'^history/proposal/(?P<pk>\d+)/$', proposal_views.ProposalHistoryCompareView.as_view(), name='proposal_history'),
    url(r'^history/filtered/(?P<pk>\d+)/$', proposal_views.ProposalFilteredHistoryCompareView.as_view(), name='proposal_filtered_history'),
    url(r'^history/approval/(?P<pk>\d+)/$', proposal_views.ApprovalHistoryCompareView.as_view(), name='approval_history'),
    url(r'^history/compliance/(?P<pk>\d+)/$', proposal_views.ComplianceHistoryCompareView.as_view(), name='compliance_history'),
    url(r'^history/helppage/(?P<pk>\d+)/$', proposal_views.HelpPageHistoryCompareView.as_view(), name='helppage_history'),
    url(r'^history/organisation/(?P<pk>\d+)/$', organisation_views.OrganisationHistoryCompareView.as_view(), name='organisation_history'),

    url(r'^proposal-payment-history/(?P<pk>[0-9]+)/', ProposalPaymentHistoryView.as_view(), name='view_proposal_payment_history'),
    url(r'^proposal-payment-history-refund/(?P<pk>[0-9]+)/', RefundProposalHistoryView.as_view(), name='view_refund_proposal_payment_history'),
    url(r'^api/check_oracle_code$', payments_api.CheckOracleCodeView.as_view(), name='check_oracle_code'),
    url(r'^api/refund_oracle$', payments_api.RefundOracleView.as_view(), name='refund_oracle'),

    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/proposal/(?P<proposal_id>\d+)/vessel_registration_documents/(?P<filename>.+)$', proposal_views.VesselRegistrationDocumentView.as_view(), name='serve_vessel_registration_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/proposal/(?P<proposal_id>\d+)/hull_identification_number_documents/(?P<filename>.+)$', proposal_views.HullIdentificationNumberDocumentView.as_view(), name='serve_hull_identification_number_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/proposal/(?P<proposal_id>\d+)/electoral_roll_documents/(?P<filename>.+)$', proposal_views.ElectoralRollDocumentView.as_view(), name='serve_electoral_roll_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/proposal/(?P<proposal_id>\d+)/insurance_certificate_documents/(?P<filename>.+)$', proposal_views.InsuranceCertificateDocumentView.as_view(), name='serve_insurance_certificate_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/proposal/(?P<proposal_id>\d+)/written_proof_documents/(?P<filename>.+)$', proposal_views.WrittenProofDocumentView.as_view(), name='serve_written_proof_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/proposal/(?P<proposal_id>\d+)/signed_licence_agreement_documents/(?P<filename>.+)$', proposal_views.SignedLicenceAgreementDocumentView.as_view(), name='serve_signed_licence_agreement_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/proposal/(?P<proposal_id>\d+)/proof_of_identity_documents/(?P<filename>.+)$', proposal_views.ProofOfIdentityDocumentView.as_view(), name='serve_proof_of_identity_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/approval/(?P<approval_id>\d+)/waiting_list_offer_documents/(?P<filename>.+)$', proposal_views.WaitingListOfferDocumentView.as_view(), name='serve_waiting_list_offer_documents'),

    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/proposal/(?P<proposal_id>\d+)/approval_documents/(?P<filename>.+)$', proposal_views.ApprovalDocumentView.as_view(), name='serve_approval_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/proposal/(?P<proposal_id>\d+)/authorised_user_summary_documents/(?P<filename>.+)$', proposal_views.AuthorisedUserSummaryDocumentView.as_view(), name='serve_authorised_user_summary_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/proposal/(?P<proposal_id>\d+)/renewal_documents/(?P<filename>.+)$', proposal_views.RenewalDocumentView.as_view(), name='serve_renewal_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/proposal/(?P<proposal_id>\d+)/approvals/communications/(?P<filename>.+)$', proposal_views.ApprovalLogDocumentView.as_view(), name='serve_approval_log_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/dcv_admission/(?P<dcv_admission_id>\d+)/dcv_admission_documents/(?P<filename>.+)$', proposal_views.DcvAdmissionDocumentView.as_view(), name='serve_dcv_admission_documents'),
    url(r'^' + PRIVATE_MEDIA_DIR_NAME + '/dcv_permit/(?P<dcv_permit_id>\d+)/dcv_permit_documents/(?P<filename>.+)$', proposal_views.DcvPermitDocumentView.as_view(), name='serve_dcv_permit_documents'),

    # Intercept the request to update the account details before reaching the ledger_api_client
    url(r'^ledger-ui/api/update-account-details/(?P<user_id>[0-9]+)/', update_personal_details, name='update-account-details'),

] + ledger_patterns + media_serv_patterns



if settings.DEBUG:  # Serve media locally in development.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if not are_migrations_running():
    DefaultDataManager()

admin.site.site_header = "RIA Mooring Licensing System Administration"
admin.site.site_title = "RIA Mooring Licensing Site"
admin.site.index_title = "RIA Mooring Licensing"

