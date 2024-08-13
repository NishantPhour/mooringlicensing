from rest_framework import serializers
from django.db.models import Sum, Max

from mooringlicensing import settings
from mooringlicensing.components.main.models import (
        CommunicationsLogEntry,
        GlobalSettings, TemporaryDocumentCollection,
        )
from ledger_api_client.ledger_models import EmailUserRO, Invoice
from ledger_api_client import utils

from mooringlicensing.ledger_api_utils import get_invoice_payment_status


class CommunicationLogEntrySerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=EmailUserRO.objects.all(),required=False)
    documents = serializers.SerializerMethodField()
    class Meta:
        model = CommunicationsLogEntry
        fields = (
            'id',
            'customer',
            'to',
            'fromm',
            'cc',
            'type',
            'reference',
            'subject'
            'text',
            'created',
            'staff',
            'proposal'
            'documents'
        )

    def get_documents(self,obj):
        return [[d.name,d._file.url] for d in obj.documents.all()]


class GlobalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalSettings
        fields = ('key', 'value')


class BookingSettlementReportSerializer(serializers.Serializer):
    date = serializers.DateTimeField(input_formats=['%d/%m/%Y'])


class OracleSerializer(serializers.Serializer):
    date = serializers.DateField(input_formats=['%d/%m/%Y','%Y-%m-%d'])
    override = serializers.BooleanField(default=False)


class InvoiceSerializer(serializers.ModelSerializer):
    payment_status = serializers.SerializerMethodField()
    invoice_url = serializers.SerializerMethodField()
    ledger_payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = (
            'id',
            'amount',
            'reference',
            'payment_status',
            'settlement_date',
            'invoice_url',
            'ledger_payment_url',
        )

    def get_payment_status(self, invoice):
        invoice_payment_status = get_invoice_payment_status(invoice.id).lower()

        if invoice_payment_status == 'unpaid':
            return 'Unpaid'
        elif invoice_payment_status == 'partially_paid':
            return 'Partially Paid'
        elif invoice_payment_status == 'paid':
            return 'Paid'
        else:
            return 'Over Paid'

    def get_invoice_url(self, invoice):
        return f'/ledger-toolkit-api/invoice-pdf/{invoice.reference}/'

    def get_ledger_payment_url(self, invoice):
        return f'{settings.LEDGER_UI_URL}/ledger/payments/oracle/payments?invoice_no={invoice.reference}'


class TemporaryDocumentCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryDocumentCollection
        fields = ('id',)

