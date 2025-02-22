from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q

import logging

from mooringlicensing.components.proposals.email import send_endorser_reminder_email
from mooringlicensing.components.main.models import NumberOfDaysType, NumberOfDaysSetting
from mooringlicensing.components.proposals.models import Proposal, AuthorisedUserApplication
from mooringlicensing.management.commands.utils import construct_email_message
from mooringlicensing.settings import CODE_DAYS_FOR_ENDORSER_AUA_REMINDER

logger = logging.getLogger('cron_tasks')
cron_email = logging.getLogger('cron_email')


class Command(BaseCommand):
    help = 'Send email to authorised user application endorser if application is not endorsed or declined within configurable number of days'

    def handle(self, *args, **options):

        errors = []
        updates = []
        today = timezone.localtime(timezone.now()).date()

        # Retrieve the number of days before expiry date of the approvals to email
        days_type = NumberOfDaysType.objects.filter(code=CODE_DAYS_FOR_ENDORSER_AUA_REMINDER).first()
        days_setting = NumberOfDaysSetting.get_setting_by_date(days_type, today)
        if not days_setting:
            # No number of days found
            raise ImproperlyConfigured("NumberOfDays: {} is not defined for the date: {}".format(days_type.name, today))
        boundary_date = today - timedelta(days=days_setting.number_of_days)

        logger.info('Running command {}'.format(__name__))

        # Construct queries
        queries = Q()
        queries &= Q(processing_status=Proposal.PROCESSING_STATUS_AWAITING_ENDORSEMENT)
        queries &= Q(lodgement_date__lt=boundary_date)

        for a in AuthorisedUserApplication.objects.filter(queries):
            try:
                send_endorser_reminder_email(a)
                a.save()
                logger.info('Reminder to endorser sent for Proposal {}'.format(a.lodgement_number))
                updates.append(a.lodgement_number)
            except Exception as e:
                err_msg = 'Error sending reminder to endorser for Proposal {}'.format(a.lodgement_number)
                logger.error('{}\n{}'.format(err_msg, str(e)))
                errors.append(err_msg)

        cmd_name = __name__.split('.')[-1].replace('_', ' ').upper()
        msg = construct_email_message(cmd_name, errors, updates)
        logger.info(msg)
        cron_email.info(msg)
