import logging
from django.core.management.base import BaseCommand
from mooringlicensing.components.proposals.models import ProposalSiteLicenseeMooringRequest, Proposal

logger = logging.getLogger('cron_tasks')

class Command(BaseCommand):
    help = 'Check Proposal Site Licensee Endorsements and Update Proposal Status'

    def handle(self, *args, **options):
        logger.info('Running command {}'.format(__name__))
        #get all enabled ProposalSiteLicenseeMooringRequests attached to a proposal with status "awaiting_endorsement"
        site_licensee_mooring_requests = ProposalSiteLicenseeMooringRequest.objects.filter(
            enabled=True,
            proposal__processing_status=Proposal.PROCESSING_STATUS_AWAITING_ENDORSEMENT
        )

        #exclude proposals that have requests that are neither declined or approved
        non_actioned_proposal_ids = list(set(list(site_licensee_mooring_requests.filter(declined_by_endorser=False,approved_by_endorser=False).values_list("proposal__id",flat=True))))

        update_proposals = Proposal.objects.filter(
            processing_status=Proposal.PROCESSING_STATUS_AWAITING_ENDORSEMENT
        ).exclude(
            id__in=non_actioned_proposal_ids
        )

        for i in update_proposals:
            logger.info(f'All site licensee mooring requests endorsed or declined for the Proposal: [{i}].')

        #any proposal with requests that are all either declined or approved are to updated to "with_assessor"
        update_proposals.update(
            processing_status=Proposal.PROCESSING_STATUS_WITH_ASSESSOR
        )

        
        