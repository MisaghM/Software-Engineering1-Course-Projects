import django.forms as forms
from .models import User, Patient, HealthCenter


class FilterForm(forms.Form):
    package_name = forms.CharField(
        max_length=100,
        label='Package Name',
        widget=forms.TextInput(attrs={'placeholder': 'Write a package name...'}),
        required=False,
    )
    center_name = forms.CharField(
        max_length=100,
        label='Health Center Name',
        widget=forms.TextInput(attrs={'placeholder': 'Write a health center name...'}),
        required=False
    )
    work_field = forms.ChoiceField(
        choices=HealthCenter.WorkField.choices,
        label='Health Center Work Field',
        required=False,
    )
    price_min = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'value': '0', 'min': '0', 'max': '1000'}),
        initial=0,
        required=False,
    )
    price_max = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'value': '1000', 'min': '0', 'max': '1000'}),
        initial=1000,
        required=False,
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        help_texts = {'username': None}
