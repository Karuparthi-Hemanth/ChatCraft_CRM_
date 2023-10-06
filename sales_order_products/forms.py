from django import forms
from .models import SalesOrderProduct

class SalesOrderProductForm(forms.ModelForm):
    class Meta:
        model = SalesOrderProduct
        fields = ["SALES_ORDER_ID", "SEQ_NUM", "PRODUCT_ID", "AMOUNT", "QUANTITY"]  # List the fields you want to edit

    def clean_SALES_ORDER_ID(self):
        sales_order = self.cleaned_data.get("SALES_ORDER_ID")
        print(sales_order)
        if sales_order.STATUS == 'invoiced':
            raise forms.ValidationError("This order is already invoiced.")
        return sales_order
    
    def clean_QUANTITY(self):
        quantity = self.cleaned_data.get("QUANTITY")
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity
    
    def clean_PRODUCT_ID(self):
        product = self.cleaned_data.get("PRODUCT_ID")
        if product.STATUS=='inactive':
            raise forms.ValidationError("Product : "+str(product)+ " cannot be inactive.")
        return product