from django.forms import ModelForm
# from .models import Order
# from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
# from django.contrib.auth.forms import User
class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    # email = forms.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ["username","first_name","last_name", "email", "password1", "password2"]

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     username = self.cleaned_data.get('username')
    #     if email and User.objects.filter(email=email).exclude(username=username).exists():
    #         raise forms.ValidationError(u'Email addresses must be unique.')
    #     return email