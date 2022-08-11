from django import forms
import datetime

from django.forms import RadioSelect, SelectDateWidget

from myapp.models import Order


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