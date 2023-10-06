from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["PRODUCT_NAME", "UOM", "QUANTITY_ON_HAND", "STATUS", "COST"]  # List the fields you want to edit

    def clean_COST(self):
        cost = self.cleaned_data.get("COST")
        if cost<0:
            raise forms.ValidationError("Cost cannot be negative.")
        return cost
    
    def clean_QUANTITY_ON_HAND(self):
        quantity_on_hand = self.cleaned_data.get("QUANTITY_ON_HAND")
        if quantity_on_hand<0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity_on_hand