from django import forms
from myapp.models import Order


class InterestForm(forms.Form):
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=[(0, 'No'), (1, 'Yes')])
    levels = forms.IntegerField(initial=1)
    comments = forms.CharField(widget=forms.Textarea(), label='Additional Comments', required=False)