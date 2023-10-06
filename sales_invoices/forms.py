from django import forms
from .models import SalesInvoice

class SalesInvoiceForm(forms.ModelForm):
    class Meta:
        model = SalesInvoice
        fields = ["SALES_ORDER_ID","STATUS","CUSTOMER_ID"]  # List the fields you want to edit

    def clean_SALES_ORDER_ID(self):
        sales_order = self.cleaned_data.get("SALES_ORDER_ID")
        if sales_order.STATUS=='invoiced':
            raise forms.ValidationError("order : "+str(sales_order)+ " is already invoiced.")
        return sales_order