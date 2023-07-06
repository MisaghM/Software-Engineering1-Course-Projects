import django.forms as forms
import django.contrib.auth.forms as aforms
from django.core.exceptions import ValidationError

from .models import HealthCenter


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


class LoginForm(aforms.AuthenticationForm):
    error_messages = {
        'invalid_login': 'Incorrect %(username)s OR password.',
        'inactive': 'Account is inactive',
    }

    def clean_username(self):
        return self.cleaned_data['username'].lower()


class SignupForm(aforms.BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs["autofocus"] = True

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if self._meta.model.objects.filter(username__iexact=username).exists():
            self._update_errors(ValidationError({
                'username': self.instance.unique_error_message(self._meta.model, ['username'])
            }))
        else:
            return username
