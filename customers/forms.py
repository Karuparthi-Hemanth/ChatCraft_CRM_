from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["COMPANY_NAME", "BALANCE_DUE", "ADDRESS", "STATUS", "CONTACT"]  # List the fields you want to edit

    def clean_BALANCE_DUE(self):
        balance = self.cleaned_data.get("BALANCE_DUE")
        if balance<0:
            raise forms.ValidationError("balance cannot be negative.")
        return balance