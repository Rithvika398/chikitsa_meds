from django import forms
from django.contrib.auth.models import User
from .models import Appt,Doctor
from django.utils import timezone


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ApptForm(forms.ModelForm):
    age=forms.IntegerField()
    #time=forms.TimeField()
    doctor=forms.CharField(max_length=50)

    class Meta:
        model = Appt
        fields = ['user', 'age', 'time', 'doctor',]
