from django import forms
from .models import SalesOrder
from datetime import datetime
class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ["CUSTOMER_ID", "ORDERDATE", "AMOUNT", "STATUS"]  # List the fields you want to edit

    def clean_CUSTOMER_ID(self):
        customer = self.cleaned_data.get("CUSTOMER_ID")
        if customer.STATUS == "inactive":
            raise forms.ValidationError("Customer :" + str(customer) + " is inactive.")
        return customer
    def clean_ORDERDATE(self):
        order_date = self.cleaned_data.get("ORDERDATE")
        print(order_date,datetime.now().date())
        if order_date<datetime.now().date():
            raise forms.ValidationError("Order date should be today or future dates.")
        return order_date