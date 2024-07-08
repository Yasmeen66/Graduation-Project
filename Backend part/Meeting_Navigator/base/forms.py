# forms.py

from django import forms
from .models import CustomUser, RecordEntry


class CustomUserForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput,label='name')
    email=forms.EmailField(widget=forms.TextInput,label='email')
    phone=forms.CharField(widget=forms.TextInput,label='phone')
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


# forms.py
from django import forms
from .models import RecordEntry, CustomUser


class RecordEntryForm(forms.ModelForm):
    meeting_name = forms.CharField(widget=forms.TextInput, label='Meeting Name')
    meeting_subject = forms.CharField(widget=forms.TextInput, label='Meeting Subject')

    class Meta:
        model = RecordEntry
        fields = ['meeting_name', 'meeting_subject']

