
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

class RegisterForm(UserCreationForm):
     email = forms.EmailField()
     class Meta:
         model = User
         field = ["username","first_name","last_name","email","password1","password2"]