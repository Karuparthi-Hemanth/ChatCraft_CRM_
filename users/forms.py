from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Import your custom user model here

class RegisterUserForm(UserCreationForm):
    user_type = forms.CharField(max_length=35)
    class Meta:
        model = User  # Specify your custom user model
        fields = ('username', 'user_type', 'password1', 'password2')  # Include the necessary fields here