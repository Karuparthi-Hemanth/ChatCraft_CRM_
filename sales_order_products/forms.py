from django import forms
from .models import SalesOrderProduct

class SalesOrderProductForm(forms.ModelForm):
    class Meta:
        model = SalesOrderProduct
        fields = ["SALES_ORDER_ID", "SEQ_NUM", "PRODUCT_ID", "AMOUNT", "QUANTITY"]  # List the fields you want to edit