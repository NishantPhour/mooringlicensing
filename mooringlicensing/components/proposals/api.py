import traceback
import os
import base64
import geojson
import json
from six.moves.urllib.parse import urlparse
from wsgiref.util import FileWrapper
from django.db.models import Q, Min
from django.db import transaction, connection
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework import viewsets, serializers, status, generics, views
from rest_framework.decorators import detail_route, list_route, renderer_classes, parser_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from django.core.cache import cache
from ledger.accounts.models import EmailUser, Address
from ledger.address.models import Country
from datetime import datetime, timedelta, date
from mooringlicensing.components.proposals.utils import save_proponent_data,save_assessor_data, proposal_submit
from mooringlicensing.components.proposals.models import searchKeyWords, search_reference, ProposalUserAction
#from mooringlicensing.utils import missing_required_fields
from mooringlicensing.components.main.utils import check_db_connection

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from mooringlicensing.components.main.models import (
        Document, #Region, District, Tenure, 
        #ApplicationType, 
        )
from mooringlicensing.components.proposals.models import (
    #ProposalType,
    Proposal,
    ProposalDocument,
    ProposalRequirement,
    ProposalStandardRequirement,
    AmendmentRequest,
    AmendmentReason,
    #Vessel,
    ChecklistQuestion,
    ProposalAssessment,
    ProposalAssessmentAnswer,
    RequirementDocument,
    WaitingListApplication,
)
from mooringlicensing.components.proposals.serializers import (
    ProposalSerializer,
    InternalProposalSerializer,
    SaveProposalSerializer,
    ProposalUserActionSerializer,
    ProposalLogEntrySerializer,
    ProposalRequirementSerializer,
    ProposalStandardRequirementSerializer,
    ProposedApprovalSerializer,
    # PropedDeclineSerializer,
    AmendmentRequestSerializer,
    # SearchReferenceSerializer,
    # SearchKeywordSerializer,
    # ListProposalSerializer,
    # AmendmentRequestDisplaySerializer,
    #VesselSerializer,
    # OnHoldSerializer,
    # ProposalOtherDetailsSerializer,
    # SaveProposalOtherDetailsSerializer,
    ChecklistQuestionSerializer,
    ProposalAssessmentSerializer,
    ProposalAssessmentAnswerSerializer, ListProposalSerializer,
)

#from mooringlicensing.components.bookings.models import Booking, ParkBooking, BookingInvoice
from mooringlicensing.components.approvals.models import Approval
from mooringlicensing.components.approvals.serializers import ApprovalSerializer
from mooringlicensing.components.compliances.models import Compliance
from mooringlicensing.components.compliances.serializers import ComplianceSerializer
from ledger.payments.invoice.models import Invoice

from mooringlicensing.helpers import is_customer, is_internal
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer
from rest_framework.filters import BaseFilterBackend
import reversion
from reversion.models import Version

import logging
logger = logging.getLogger(__name__)


#class GetProposalType(views.APIView):
#    renderer_classes = [JSONRenderer, ]
#
#    def get(self, request, format=None):
#        _type = ProposalType.objects.first()
#        if _type:
#            serializer = ProposalTypeSerializer(_type)
#            return Response(serializer.data)
#        else:
#            return Response({'error': 'There is currently no application type.'}, status=status.HTTP_404_NOT_FOUND)


class GetApplicationTypeDescriptions(views.APIView):
    renderer_classes = [JSONRenderer, ]

    def get(self, request, format=None):
        #serializer = ApplicationTypeDescriptionsSerializer(Proposal.application_type_descriptions(), many=True)
        #return Response(serializer.data)
        return Response(Proposal.application_type_descriptions())


class GetApplicationTypeDict(views.APIView):
    renderer_classes = [JSONRenderer, ]

    def get(self, request, format=None):
        apply_page = request.GET.get('apply_page', 'false')
        apply_page = True if apply_page.lower() in ['true', 'yes', 'y', ] else False
        return Response(Proposal.application_types_dict(apply_page=apply_page))


class GetApplicationStatusesDict(views.APIView):
    renderer_classes = [JSONRenderer, ]

    def get(self, request, format=None):
        data = [{'code': i[0], 'description': i[1]} for i in Proposal.CUSTOMER_STATUS_CHOICES]
        return Response(data)


class GetEmptyList(views.APIView):
    renderer_classes = [JSONRenderer, ]

    def get(self, request, format=None):
        return Response([])


class VersionableModelViewSetMixin(viewsets.ModelViewSet):
    @detail_route(methods=['GET',])
    def history(self, request, *args, **kwargs):
        _object = self.get_object()
        #_versions = reversion.get_for_object(_object)
        _versions = Version.objects.get_for_object(_object)

        _context = {
            'request': request
        }

        #_version_serializer = VersionSerializer(_versions, many=True, context=_context)
        _version_serializer = ProposalSerializer([v.object for v in _versions], many=True, context=_context)
        # TODO
        # check pagination
        return Response(_version_serializer.data)


class ProposalFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()

        filter_application_type = request.GET.get('filter_application_type')
        if filter_application_type and not filter_application_type.lower() == 'all':
            q = None
            for item in Proposal.__subclasses__():
                if hasattr(item, 'code') and item.code == filter_application_type:
                    lookup = "{}__isnull".format(item._meta.model_name)
                    q = Q(**{lookup: False})
                    break
            queryset = queryset.filter(q) if q else queryset

        filter_application_status = request.GET.get('filter_application_status')
        if filter_application_status and not filter_application_status.lower() == 'all':
            queryset = queryset.filter(customer_status=filter_application_status)

        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        try:
            queryset = super(ProposalFilterBackend, self).filter_queryset(request, queryset, view)
        except Exception as e:
            print(e)
        setattr(view, '_datatables_total_count', total_count)
        return queryset


class ProposalRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        return super(ProposalRenderer, self).render(data, accepted_media_type, renderer_context)


class ProposalPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (ProposalFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (ProposalRenderer,)
    queryset = Proposal.objects.none()
    serializer_class = ListProposalSerializer
    search_fields = ['lodgement_number', ]
    page_size = 10

    def get_queryset(self):
        request_user = self.request.user
        if is_internal(self.request):
            return Proposal.objects.all()
        elif is_customer(self.request):
            qs = Proposal.objects.filter(Q(submitter=request_user))
            return qs
        return Proposal.objects.none()

    @list_route(methods=['GET',])
    def list_external(self, request, *args, **kwargs):
        """
        User is accessing /external/ page
        """
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        # on the internal organisations dashboard, filter the Proposal/Approval/Compliance datatables by applicant/organisation
        # applicant_id = request.GET.get('org_id')
        # if applicant_id:
        #     qs = qs.filter(applicant_id=applicant_id)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListProposalSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class WaitingListApplicationViewSet(viewsets.ModelViewSet):
    queryset = WaitingListApplication.objects.none()
    serializer_class = ProposalSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            qs = WaitingListApplication.objects.all()
            return qs
        elif is_customer(self.request):
            #user_orgs = [org.id for org in user.mooringlicensing_organisations.all()]
            queryset = WaitingListApplication.objects.filter(Q(proxy_applicant_id=user.id) | Q(submitter=user))
            return queryset
        logger.warn("User is neither customer nor internal user: {} <{}>".format(user.get_full_name(), user.email))
        return WaitingListApplication.objects.none()

    def create(self, request, *args, **kwargs):
        obj = WaitingListApplication.objects.create(
                submitter=request.user,
                )
        serialized_obj = ProposalSerializer(obj)
        return Response(serialized_obj.data)


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.none()
    serializer_class = ProposalSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            qs = Proposal.objects.all()
            return qs
        elif is_customer(self.request):
            user_orgs = [org.id for org in user.mooringlicensing_organisations.all()]
            queryset = Proposal.objects.filter(Q(org_applicant_id__in=user_orgs) | Q(submitter=user))
            return queryset
        logger.warn("User is neither customer nor internal user: {} <{}>".format(user.get_full_name(), user.email))
        return Proposal.objects.none()

    def get_object(self):

        check_db_connection()
        try:
            obj = super(ProposalViewSet, self).get_object()
        except Exception as e:
            # because current queryset excludes migrated licences
            obj = get_object_or_404(Proposal, id=self.kwargs['id'])
        return obj

    #def get_serializer_class(self):
    #    try:
    #        application_type = Proposal.objects.get(id=self.kwargs.get('id')).application_type.name
    #        if application_type == ApplicationType.TCLASS:
    #            return ProposalSerializer
    #        elif application_type == ApplicationType.FILMING:
    #            return ProposalFilmingSerializer
    #        elif application_type == ApplicationType.EVENT:
    #            return ProposalEventSerializer
    #    except serializers.ValidationError:
    #        print(traceback.print_exc())
    #        raise
    #    except ValidationError as e:
    #        if hasattr(e,'error_dict'):
    #            raise serializers.ValidationError(repr(e.error_dict))
    #        else:
    #            if hasattr(e,'message'):
    #                raise serializers.ValidationError(e.message)
    #    except Exception as e:
    #        print(traceback.print_exc())
    #        raise serializers.ValidationError(str(e))

    #def internal_serializer_class(self):
    #    try:
    #        application_type = Proposal.objects.get(id=self.kwargs.get('id')).application_type.name
    #        if application_type == ApplicationType.TCLASS:
    #            return InternalProposalSerializer
    #        elif application_type == ApplicationType.FILMING:
    #            return InternalFilmingProposalSerializer
    #        elif application_type == ApplicationType.EVENT:
    #            return InternalEventProposalSerializer
    #    except serializers.ValidationError:
    #        print(traceback.print_exc())
    #        raise
    #    except ValidationError as e:
    #        if hasattr(e,'error_dict'):
    #            raise serializers.ValidationError(repr(e.error_dict))
    #        else:
    #            if hasattr(e,'message'):
    #                raise serializers.ValidationError(e.message)
    #    except Exception as e:
    #        print(traceback.print_exc())
    #        raise serializers.ValidationError(str(e))


    #@list_route(methods=['GET',])
    #def filter_list(self, request, *args, **kwargs):
    #    """ Used by the internal/external dashboard filters """
    #    region_qs =  self.get_queryset().filter(region__isnull=False).values_list('region__name', flat=True).distinct()
    #    #district_qs =  self.get_queryset().filter(district__isnull=False).values_list('district__name', flat=True).distinct()
    #    activity_qs =  self.get_queryset().filter(activity__isnull=False).values_list('activity', flat=True).distinct()
    #    submitter_qs = self.get_queryset().filter(submitter__isnull=False).distinct('submitter__email').values_list('submitter__first_name','submitter__last_name','submitter__email')
    #    submitters = [dict(email=i[2], search_term='{} {} ({})'.format(i[0], i[1], i[2])) for i in submitter_qs]
    #    application_types=ApplicationType.objects.filter(visible=True).values_list('name', flat=True)
    #    data = dict(
    #        regions=region_qs,
    #        #districts=district_qs,
    #        activities=activity_qs,
    #        submitters=submitters,
    #        application_types=application_types,
    #        #processing_status_choices = [i[1] for i in Proposal.PROCESSING_STATUS_CHOICES],
    #        #processing_status_id_choices = [i[0] for i in Proposal.PROCESSING_STATUS_CHOICES],
    #        #customer_status_choices = [i[1] for i in Proposal.CUSTOMER_STATUS_CHOICES],
    #        approval_status_choices = [i[1] for i in Approval.STATUS_CHOICES],
    #    )
    #    return Response(data)

    @detail_route(methods=['GET',])
    def compare_list(self, request, *args, **kwargs):
        """ Returns the reversion-compare urls --> list"""
        current_revision_id = Version.objects.get_for_object(self.get_object()).first().revision_id
        versions = Version.objects.get_for_object(self.get_object()).select_related("revision__user").filter(Q(revision__comment__icontains='status') | Q(revision_id=current_revision_id))
        version_ids = [i.id for i in versions]
        urls = ['?version_id2={}&version_id1={}'.format(version_ids[0], version_ids[i+1]) for i in range(len(version_ids)-1)]
        return Response(urls)

    @detail_route(methods=['GET',])
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = ProposalUserActionSerializer(qs,many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',])
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = ProposalLogEntrySerializer(qs,many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    @renderer_classes((JSONRenderer,))
    def add_comms_log(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                mutable=request.data._mutable
                request.data._mutable=True
                request.data['proposal'] = u'{}'.format(instance.id)
                request.data['staff'] = u'{}'.format(request.user.id)
                request.data._mutable=mutable
                serializer = ProposalLogEntrySerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                comms = serializer.save()
                # Save the files
                for f in request.FILES:
                    document = comms.documents.create()
                    document.name = str(request.FILES[f])
                    document._file = request.FILES[f]
                    document.save()
                # End Save Documents

                return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',])
    def requirements(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            #qs = instance.requirements.all()
            qs = instance.requirements.all().exclude(is_deleted=True)
            qs=qs.order_by('order')
            serializer = ProposalRequirementSerializer(qs,many=True, context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',])
    def amendment_request(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.amendment_requests
            qs = qs.filter(status = 'requested')
            serializer = AmendmentRequestDisplaySerializer(qs,many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @list_route(methods=['GET',])
    def user_list(self, request, *args, **kwargs):
        qs = self.get_queryset().exclude(processing_status='discarded')
        #serializer = DTProposalSerializer(qs, many=True)
        serializer = ListProposalSerializer(qs,context={'request':request}, many=True)
        return Response(serializer.data)

    @list_route(methods=['GET',])
    def user_list_paginated(self, request, *args, **kwargs):
        """
        Placing Paginator class here (instead of settings.py) allows specific method for desired behaviour),
        otherwise all serializers will use the default pagination class

        https://stackoverflow.com/questions/29128225/django-rest-framework-3-1-breaks-pagination-paginationserializer
        """
        proposals = self.get_queryset().exclude(processing_status='discarded')
        paginator = DatatablesPageNumberPagination()
        paginator.page_size = proposals.count()
        result_page = paginator.paginate_queryset(proposals, request)
        serializer = ListProposalSerializer(result_page, context={'request':request}, many=True)
        return paginator.get_paginated_response(serializer.data)

    @detail_route(methods=['GET',])
    def internal_proposal(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = InternalProposalSerializer(instance,context={'request':request})
        if instance.application_type.name==ApplicationType.TCLASS:
            serializer = InternalProposalSerializer(instance,context={'request':request})
        elif instance.application_type.name==ApplicationType.FILMING:
            serializer = InternalFilmingProposalSerializer(instance,context={'request':request})
        elif instance.application_type.name==ApplicationType.EVENT:
            serializer = InternalEventProposalSerializer(instance,context={'request':request})
        return Response(serializer.data)

    @detail_route(methods=['post'])
    @renderer_classes((JSONRenderer,))
    def submit(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            #instance.submit(request,self)
            proposal_submit(instance, request)
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
            #return redirect(reverse('external'))
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',])
    def assign_request_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.assign_officer(request,request.user)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    def assign_to(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_id = request.data.get('assessor_id',None)
            user = None
            if not user_id:
                raise serializers.ValidationError('An assessor id is required')
            try:
                user = EmailUser.objects.get(id=user_id)
            except EmailUser.DoesNotExist:
                raise serializers.ValidationError('A user with the id passed in does not exist')
            instance.assign_officer(request,user)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',])
    def unassign(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.unassign(request)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    def switch_status(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            status = request.data.get('status')
            approver_comment = request.data.get('approver_comment')
            if not status:
                raise serializers.ValidationError('Status is required')
            else:
                if not status in ['with_assessor','with_assessor_requirements','with_approver']:
                    raise serializers.ValidationError('The status provided is not allowed')
            instance.move_to_status(request,status, approver_comment)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
            # if instance.application_type.name==ApplicationType.TCLASS:
            #     serializer = InternalProposalSerializer(instance,context={'request':request})
            # elif instance.application_type.name==ApplicationType.FILMING:
            #     serializer = InternalFilmingProposalSerializer(instance,context={'request':request})
            # elif instance.application_type.name==ApplicationType.EVENT:
            #     serializer = InternalProposalSerializer(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    def reissue_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            status = request.data.get('status')
            if not status:
                raise serializers.ValidationError('Status is required')
            else:
                if instance.application_type.name==ApplicationType.FILMING and instance.filming_approval_type=='lawful_authority':
                    status='with_assessor'
                else:
                    if not status in ['with_approver']:
                        raise serializers.ValidationError('The status provided is not allowed')
            instance.reissue_approval(request,status)
            serializer = InternalProposalSerializer(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',])
    def renew_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance = instance.renew_approval(request)
            serializer = SaveProposalSerializer(instance,context={'request':request})
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)

    @detail_route(methods=['GET',])
    def amend_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance = instance.amend_approval(request)
            serializer = SaveProposalSerializer(instance,context={'request':request})
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)

    @detail_route(methods=['POST',])
    def proposed_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ProposedApprovalSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.proposed_approval(request,serializer.validated_data)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    def approval_level_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance = instance.assing_approval_level_document(request)
            serializer = InternalProposalSerializer(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    def final_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ProposedApprovalSerializer(data=request.data)
            #import ipdb; ipdb.set_trace()
            serializer.is_valid(raise_exception=True)
            instance.final_approval(request,serializer.validated_data)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    def proposed_decline(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = PropedDeclineSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.proposed_decline(request,serializer.validated_data)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    def final_decline(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = PropedDeclineSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.final_decline(request,serializer.validated_data)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    #@detail_route(methods=['POST',])
    #@renderer_classes((JSONRenderer,))
    #def on_hold(self, request, *args, **kwargs):
    #    try:
    #        with transaction.atomic():
    #            instance = self.get_object()
    #            is_onhold =  eval(request.data.get('onhold'))
    #            data = {}
    #            if is_onhold:
    #                data['type'] = u'onhold'
    #                instance.on_hold(request)
    #            else:
    #                data['type'] = u'onhold_remove'
    #                instance.on_hold_remove(request)

    #            data['proposal'] = u'{}'.format(instance.id)
    #            data['staff'] = u'{}'.format(request.user.id)
    #            data['text'] = request.user.get_full_name() + u': {}'.format(request.data['text'])
    #            data['subject'] = request.user.get_full_name() + u': {}'.format(request.data['text'])
    #            serializer = ProposalLogEntrySerializer(data=data)
    #            serializer.is_valid(raise_exception=True)
    #            comms = serializer.save()

    #            # save the files
    #            documents_qs = instance.onhold_documents.filter(input_name='on_hold_file', visible=True)
    #            for f in documents_qs:
    #                document = comms.documents.create(_file=f._file, name=f.name)
    #                #document = comms.documents.create()
    #                #document.name = f.name
    #                #document._file = f._file #.strip('/media')
    #                document.input_name = f.input_name
    #                document.can_delete = True
    #                document.save()
    #            # end save documents

    #            return Response(serializer.data)
    #    except serializers.ValidationError:
    #        print(traceback.print_exc())
    #        raise
    #    except ValidationError as e:
    #        print(traceback.print_exc())
    #        raise serializers.ValidationError(repr(e.error_dict))
    #    except Exception as e:
    #        print(traceback.print_exc())
    #        raise serializers.ValidationError(str(e))

    @detail_route(methods=['post'])
    @renderer_classes((JSONRenderer,))
    def draft(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            save_proponent_data(instance,request,self)
            return redirect(reverse('external'))
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
        raise serializers.ValidationError(str(e))

    @detail_route(methods=['post'])
    @renderer_classes((JSONRenderer,))
    def assessor_save(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            save_assessor_data(instance,request,self)
            return redirect(reverse('external'))
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def create(self, request, *args, **kwargs):
        raise NotImplementedError("Parent objects should not be created directly")

    def update(self, request, *args, **kwargs):
        try:
            http_status = status.HTTP_200_OK
            instance = self.get_object()
            #if application_name==ApplicationType.TCLASS:
            #    serializer = SaveProposalSerializer(instance,data=request.data)
            #elif application_name==ApplicationType.FILMING:
            #    serializer=ProposalFilmingOtherDetailsSerializer(data=other_details_data)
            #elif application_name==ApplicationType.EVENT:
            #    serializer=ProposalEventOtherDetailsSerializer(data=other_details_data)

            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def destroy(self, request,*args,**kwargs):
        try:
            http_status = status.HTTP_200_OK
            instance = self.get_object()
            serializer = SaveProposalSerializer(instance,{'processing_status':'discarded', 'previous_application': None},partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data,status=http_status)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class ProposalRequirementViewSet(viewsets.ModelViewSet):
    #queryset = ProposalRequirement.objects.all()
    queryset = ProposalRequirement.objects.none()
    serializer_class = ProposalRequirementSerializer

    def get_queryset(self):
        qs = ProposalRequirement.objects.all().exclude(is_deleted=True)
        return qs

    @detail_route(methods=['GET',])
    def move_up(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.up()
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',])
    def move_down(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.down()
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',])
    def discard(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    @renderer_classes((JSONRenderer,))
    def delete_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            RequirementDocument.objects.get(id=request.data.get('id')).delete()
            return Response([dict(id=i.id, name=i.name,_file=i._file.url) for i in instance.requirement_documents.all()])
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            instance.add_documents(request)
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


    def create(self, request, *args, **kwargs):
        try:
#            data = {
#                'due_date': request.data.get('due_date'),
#                'standard': request.data.get('standard'),
#                'recurrence': reqeust.data.get('recurrence'),
#                'recurrence_pattern': request.data.get('recurrence_pattern'),
#                'proposal': request.data.get('proposal'),
#                'referral_group': request.data.get('referral_group'),
#            }

            #serializer = self.get_serializer(data= request.data)
            serializer = self.get_serializer(data= json.loads(request.data.get('data')))
            #serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception = True)
            instance = serializer.save()
            instance.add_documents(request)
            #serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class ProposalStandardRequirementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProposalStandardRequirement.objects.all()
    serializer_class = ProposalStandardRequirementSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(text__icontains=search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class AmendmentRequestViewSet(viewsets.ModelViewSet):
    queryset = AmendmentRequest.objects.all()
    serializer_class = AmendmentRequestSerializer

    def create(self, request, *args, **kwargs):
        try:
            reason_id=request.data.get('reason')
            data = {
                #'schema': qs_proposal_type.order_by('-version').first().schema,
                'text': request.data.get('text'),
                'proposal': request.data.get('proposal'),
                'reason': AmendmentReason.objects.get(id=reason_id) if reason_id else None,
            }
            serializer = self.get_serializer(data= request.data)
            #serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception = True)
            instance = serializer.save()
            instance.generate_amendment(request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


#class AccreditationTypeView(views.APIView):
#
#    renderer_classes = [JSONRenderer,]
#    def get(self,request, format=None):
#        choices_list = []
#        #choices = ProposalOtherDetails.ACCREDITATION_TYPE_CHOICES
#        choices=ProposalAccreditation.ACCREDITATION_TYPE_CHOICES
#        if choices:
#            for c in choices:
#                choices_list.append({'key': c[0],'value': c[1]})
#        return Response(choices_list)
#
#class LicencePeriodChoicesView(views.APIView):
#
#    renderer_classes = [JSONRenderer,]
#    def get(self,request, format=None):
#        choices_list = []
#        choices = ProposalOtherDetails.LICENCE_PERIOD_CHOICES
#        if choices:
#            for c in choices:
#                choices_list.append({'key': c[0],'value': c[1]})
#        return Response(choices_list)


class AmendmentRequestReasonChoicesView(views.APIView):

    renderer_classes = [JSONRenderer,]
    def get(self,request, format=None):
        choices_list = []
        #choices = AmendmentRequest.REASON_CHOICES
        choices=AmendmentReason.objects.all()
        if choices:
            for c in choices:
                #choices_list.append({'key': c[0],'value': c[1]})
                choices_list.append({'key': c.id,'value': c.reason})
        return Response(choices_list)


class SearchKeywordsView(views.APIView):
    renderer_classes = [JSONRenderer,]
    def post(self,request, format=None):
        qs = []
        searchWords = request.data.get('searchKeywords')
        searchProposal = request.data.get('searchProposal')
        searchApproval = request.data.get('searchApproval')
        searchCompliance = request.data.get('searchCompliance')
        if searchWords:
            qs= searchKeyWords(searchWords, searchProposal, searchApproval, searchCompliance)
        #queryset = list(set(qs))
        serializer = SearchKeywordSerializer(qs, many=True)
        return Response(serializer.data)

class SearchReferenceView(views.APIView):
    renderer_classes = [JSONRenderer,]
    def post(self,request, format=None):
        try:
            qs = []
            reference_number = request.data.get('reference_number')
            if reference_number:
                qs= search_reference(reference_number)
            #queryset = list(set(qs))
            serializer = SearchReferenceSerializer(qs)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                print(e)
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


#class VesselViewSet(viewsets.ModelViewSet):
#    queryset = Vessel.objects.all().order_by('id')
#    serializer_class = VesselSerializer
#
#    @detail_route(methods=['post'])
#    def edit_vessel(self, request, *args, **kwargs):
#        try:
#            instance = self.get_object()
#            serializer = VesselSerializer(instance, data=request.data)
#            serializer.is_valid(raise_exception=True)
#            serializer.save()
#            instance.proposal.log_user_action(ProposalUserAction.ACTION_EDIT_VESSEL.format(instance.id),request)
#            return Response(serializer.data)
#        except serializers.ValidationError:
#            print(traceback.print_exc())
#            raise
#        except ValidationError as e:
#            if hasattr(e,'error_dict'):
#                raise serializers.ValidationError(repr(e.error_dict))
#            else:
#                if hasattr(e,'message'):
#                    raise serializers.ValidationError(e.message)
#        except Exception as e:
#            print(traceback.print_exc())
#            raise serializers.ValidationError(str(e))
#
#    def create(self, request, *args, **kwargs):
#        try:
#            #instance = self.get_object()
#            serializer = VesselSerializer(data=request.data)
#            serializer.is_valid(raise_exception=True)
#            instance=serializer.save()
#            instance.proposal.log_user_action(ProposalUserAction.ACTION_CREATE_VESSEL.format(instance.id),request)
#            return Response(serializer.data)
#        except serializers.ValidationError:
#            print(traceback.print_exc())
#            raise
#        except ValidationError as e:
#            if hasattr(e,'error_dict'):
#                raise serializers.ValidationError(repr(e.error_dict))
#            else:
#                if hasattr(e,'message'):
#                    raise serializers.ValidationError(e.message)
#        except Exception as e:
#            print(traceback.print_exc())
#            raise serializers.ValidationError(str(e))

class AssessorChecklistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChecklistQuestion.objects.none()
    serializer_class = ChecklistQuestionSerializer

    def get_queryset(self):
        qs=ChecklistQuestion.objects.filter(Q(list_type = 'assessor_list')& Q(obsolete=False))
        return qs

class ProposalAssessmentViewSet(viewsets.ModelViewSet):
    #queryset = ProposalRequirement.objects.all()
    queryset = ProposalAssessment.objects.all()
    serializer_class = ProposalAssessmentSerializer

    @detail_route(methods=['post'])
    def update_assessment(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            request.data['submitter']= request.user.id
            serializer = ProposalAssessmentSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            checklist=request.data['checklist']
            if checklist:
                for chk in checklist:
                    try:
                        chk_instance=ProposalAssessmentAnswer.objects.get(id=chk['id'])
                        serializer_chk = ProposalAssessmentAnswerSerializer(chk_instance, data=chk)
                        serializer_chk.is_valid(raise_exception=True)
                        serializer_chk.save()
                    except:
                        raise
            #instance.proposal.log_user_action(ProposalUserAction.ACTION_EDIT_VESSEL.format(instance.id),request)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

