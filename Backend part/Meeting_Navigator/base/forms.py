# forms.py

from django import forms
from .models import CustomUser


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone', 'password']
        labels = {
            'name': 'Name',
            'email': 'Email',
            'phone': 'Phone',
            'password': 'Password',
        }
