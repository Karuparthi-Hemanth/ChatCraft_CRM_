from django import forms
from .models import SalesInvoice

class SalesInvoiceForm(forms.ModelForm):
    class Meta:
        model = SalesInvoice
        fields = ["SALES_ORDER_ID", "CUSTOMER_ID", "TOTAL_AMOUNT", "TOTAL_ITEMS","INVOICE_DATE","STATUS"]  # List the fields you want to edit