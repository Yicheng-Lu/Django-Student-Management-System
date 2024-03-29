from django import forms
import datetime

from django.contrib.auth.forms import UserCreationForm
from django.forms import RadioSelect, SelectDateWidget
from django.forms import ModelForm

from myapp.models import *


class InterestForm(forms.Form):
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=[(0, 'No'), (1, 'Yes')])
    levels = forms.IntegerField(initial=1)
    comments = forms.CharField(widget=forms.Textarea(), label='Additional Comments', required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'course', 'levels', 'order_date']
        widgets = {
            'student': RadioSelect,
            'order_date': SelectDateWidget,
        }


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='username', max_length=100)
    password = forms.CharField(required=True, label='password', max_length=20)


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Student
        fields = ['username', 'first_name', 'last_name', 'school', 'address', 'city', 'interested_in']


class ProfileUploadHandler(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_name', 'profile_storage']
