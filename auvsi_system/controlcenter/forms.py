from django import forms
from django.db import models
from .models import InteropServer


class InteropServerForm(forms.ModelForm):
    class Meta:
        model = InteropServer
        fields = ('url', 'username', 'password')

class MainPageForm(forms.Form):
    flush_data = forms.CharField(label='Flush data', max_length=20)