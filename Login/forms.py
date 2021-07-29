

from django import forms
from django.forms import widgets
from django import forms
from django.forms.fields import ChoiceField


class loginPage(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    