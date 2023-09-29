from django import forms
from .models import CustomerLedgerEntry

class CustomerLedgerEntryForm(forms.ModelForm):
    class Meta:
        model = CustomerLedgerEntry
        fields = ["CUSTOMER_LEDGER_ENTRY_ID", "CUSTOMER_ID", "SALES_INVOICE_ID", "AMOUNT", "PAID_DATE"]  # List the fields you want to edit