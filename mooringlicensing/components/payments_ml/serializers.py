from rest_framework import serializers

from mooringlicensing.components.approvals.models import DcvPermit


class DcvPermitSerializer(serializers.ModelSerializer):
    dcv_vessel_id = serializers.IntegerField(required=True)
    dcv_organisation_id = serializers.IntegerField(required=True)
    fee_season_id = serializers.IntegerField(required=True)

    def validate(self, data):
        field_errors = {}
        non_field_errors = []

        if not self.partial:
            if not data['fee_season_id']:
                field_errors['year'] = ['Please select a year.',]
            # if not data['period_to']:
            #     field_errors['Period to'] = ['Please select a date.',]
            # # if not data['apiary_site_id'] and not data['apiary_site_id'] > 0:
            # #     field_errors['Site'] = ['Please select a site',]
            # if not data['comments']:
            #     field_errors['comments'] = ['Please enter comments.',]

            dcv_permit_qs = DcvPermit.objects.filter(dcv_vessel_id=data.get('dcv_vessel_id', 0), fee_season_id=data.get('fee_season_id', 0))
            if dcv_permit_qs:
                non_field_errors.append('This vessel already has a DCV Permit for the given year.')

            # Raise errors
            if field_errors:
                raise serializers.ValidationError(field_errors)
            if non_field_errors:
                raise serializers.ValidationError(non_field_errors)
        else:
            # Partial udpate, which means the dict data doesn't have all the field
            pass

        return data

    class Meta:
        model = DcvPermit
        fields = (
            'id',
            'lodgement_number',
            'submitter',
            'lodgement_datetime',
            'dcv_vessel_id',
            'dcv_organisation_id',
            'fee_season_id',
        )
        read_only_fields = (
            'id',
            'lodgement_number',
        )
