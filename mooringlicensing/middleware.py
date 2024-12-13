from django.urls import reverse
from django.shortcuts import redirect
from urllib.parse import quote_plus
from django.http import HttpResponse
import hashlib
import re
from reversion.middleware  import RevisionMiddleware
from reversion.views import _request_creates_revision
from ledger_api_client.managed_models import SystemUser, SystemUserAddress
from django.core.exceptions import ObjectDoesNotExist
from mooringlicensing.helpers import is_internal
from mooringlicensing.components.proposals.models import Proposal

import logging

logger = logging.getLogger(__name__)

CHECKOUT_PATH = re.compile('^/ledger/checkout/checkout')

class FirstTimeNagScreenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.user.is_authenticated 
            and request.method == 'GET' 
            and 'api' not in request.path 
            and 'admin' not in request.path 
            and 'static' not in request.path
            and "/ledger-ui/" not in request.get_full_path()):
            path_first_time = '/ledger-ui/system-accounts-firsttime'
            path_logout = reverse('logout')
            system_user_exists = True
            try:
                system_user = SystemUser.objects.get(ledger_id=request.user)
            except ObjectDoesNotExist:
                system_user_exists = False

            if system_user_exists:
                system_user_addresses = SystemUserAddress.objects.filter(system_user=system_user)
                residential_address = system_user_addresses.filter(address_type=SystemUserAddress.ADDRESS_TYPE[0][0])
                postal_address = system_user_addresses.filter(address_type=SystemUserAddress.ADDRESS_TYPE[1][0])

            if (not system_user_exists or
                not system_user.legal_first_name or 
                not system_user.legal_last_name or 
                not system_user.legal_dob or
                not residential_address.exists() or 
                not postal_address.exists() or
                not system_user.mobile_number
                ):
                # We don't want to redirect the user when the user is accessing the firsttime page or logout page.
                if request.path not in (path_logout):
                    logger.info('redirect')
                    return redirect(path_first_time + "?next=" + quote_plus(request.get_full_path()))
                    
        response = self.get_response(request)
        return response


class CacheControlMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path[:5] == '/api/' or request.path == '/':
            response['Cache-Control'] = 'private, no-store'
        elif request.path[:8] == '/static/':
            response['Cache-Control'] = 'public, max-age=300'
        return response


class RevisionOverrideMiddleware(RevisionMiddleware):

    """
        Wraps the entire request in a revision.

        override venv/lib/python2.7/site-packages/reversion/middleware.py
    """

	# exclude ledger payments/checkout from revision - hack to overcome basket (lagging status) issue/conflict with reversion
    def request_creates_revision(self, request):
        return _request_creates_revision(request) and 'checkout' not in request.get_full_path()

class PaymentSessionMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):

        redirect_path = 'internal' if is_internal(request) else 'external'

        if (request.user.is_authenticated 
        and (CHECKOUT_PATH.match(request.path)
        or request.path.startswith("/ledger-api/process-payment") 
        or request.path.startswith('/ledger-api/payment-details'))):
            #TODO what about DCVs or sticker replacements?
            if 'ml_proposal' in request.session:
                if request.path.startswith("/ledger-api/process-payment"):

                    checkouthash =  hashlib.sha256(str(request.session["ml_proposal"]).encode('utf-8')).hexdigest() 
                    checkouthash_cookie = request.COOKIES.get('checkouthash')
                    validation_cookie = request.COOKIES.get(request.POST['payment-csrfmiddlewaretoken'])

                    proposal_count = Proposal.objects.filter(pk=request.session['ml_proposal']).count()
                    if checkouthash_cookie != checkouthash or checkouthash_cookie != validation_cookie or proposal_count == 0:                         
                        url_redirect = reverse(redirect_path)
                        response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
                        return response  
            else:
                 if request.path.startswith("/ledger-api/process-payment"):# or request.path.startswith('/ledger-api/payment-details'):
                    url_redirect = reverse(redirect_path)
                    response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
                    return response
                 
        return None


    def __call__(self, request):
        
        response= self.get_response(request)
        redirect_path = 'internal' if is_internal(request) else 'external'
        
        if (request.user.is_authenticated 
        and (CHECKOUT_PATH.match(request.path)
        or request.path.startswith("/ledger-api/process-payment") 
        or request.path.startswith('/ledger-api/payment-details'))):
            #TODO what about DCVs or sticker replacements?
            if 'ml_proposal' in request.session:
                try:
                    proposal = Proposal.objects.get(pk=request.session['ml_proposal'])
                except:
                    # no idea what object is in self.request.session['ml_proposal'], ditch it
                    del request.session['ml_proposal']
                    return response

                if request.path.startswith("/ledger-api/process-payment"):# or request.path.startswith('/ledger-api/payment-details'):      
                    
                    if "ml_proposal" not in request.session:
                         url_redirect = reverse(redirect_path)
                         response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
                         return response    

                    checkouthash =  hashlib.sha256(str(request.session["ml_proposal"]).encode('utf-8')).hexdigest() 
                    checkouthash_cookie = request.COOKIES.get('checkouthash')
                    validation_cookie = request.COOKIES.get(request.POST['payment-csrfmiddlewaretoken'])

                    proposal_count = Proposal.objects.filter(pk=request.session['ml_proposal']).count()
                    if checkouthash_cookie != checkouthash or checkouthash_cookie != validation_cookie or proposal_count == 0:                         
                         url_redirect = reverse(redirect_path)
                         response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
                         return response                                                                                                 
            else:
                 if request.path.startswith("/ledger-api/process-payment"):# or request.path.startswith('/ledger-api/payment-details'):
                    url_redirect = reverse(redirect_path)
                    response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
                    return response

            # force a redirect if in the checkout
            if ('ml_proposal' not in request.session) and CHECKOUT_PATH.match(request.path):
                url_redirect = reverse(redirect_path)
                response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
                return response
                
        return response