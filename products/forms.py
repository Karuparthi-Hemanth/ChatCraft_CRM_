from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["PRODUCT_NAME", "UOM", "QUANTITY_ON_HAND", "STATUS", "COST"]  # List the fields you want to edit