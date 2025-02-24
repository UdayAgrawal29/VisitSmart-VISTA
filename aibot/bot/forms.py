from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Login

# bot/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = Login
        fields = ('username', 'email', 'password1', 'password2')
