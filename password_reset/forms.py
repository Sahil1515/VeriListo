

from django import forms
from django import forms


class password_reset(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    