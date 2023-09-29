from django import forms
from .models import SalesOrder

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ["CUSTOMER_ID", "ORDERDATE", "AMOUNT", "STATUS"]  # List the fields you want to edit

