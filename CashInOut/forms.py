from .models import CashIn, CashOut, Profile
from django.forms import ModelForm
from django.forms import TextInput, Textarea
from django import forms


class ProfileNameField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', '')
        kwargs.setdefault('widget', forms.TextInput(attrs={'class': 'profile-name-field', 'placeholder': 'Name'}))
        super().__init__(*args, **kwargs)

    def clean(self, value):
        profile_name = value.strip()
        try:
            profile = Profile.objects.get(profile_name=profile_name)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(profile_name=profile_name)
        return profile


class CashInForm(ModelForm):
    name = ProfileNameField(max_length=255)

    class Meta:
        model = CashIn
        fields = ['name', 'cash_in', 'reference_no']
        labels = {
            "name": "",
            "cash_in": "",
            "reference_no": "",
        }
        widgets = {
            'name': TextInput(attrs={
                'class': "cash-in-field",
                'placeholder': 'Name'
            }),
            'reference_no': TextInput(attrs={
                'class': "cash-in-field",
                'placeholder': 'Reference Number'
            }),
            'cash_in': forms.NumberInput(attrs={
                'class': "cash-in-field",
                'placeholder': 'Cash In Amount'
            }),
        }


class CashOutForm(ModelForm):
    name = ProfileNameField(max_length=255)

    class Meta:
        model = CashOut
        fields = ['name', 'cash_out', 'reference_no']
        labels = {
            "name": "",
            "cash_out": "",
            "reference_no": "",
        }
        widgets = {
            'reference_no': TextInput(attrs={
                'class': "cash-out-field",
                'placeholder': 'Reference Number'
            }),
            'name': TextInput(attrs={
                'class': "cash-out-field",
                'placeholder': 'Name'
            }),
            'cash_out': forms.NumberInput(attrs={
                'class': "cash-out-field",
                'placeholder': 'Cash Out Amount'
            }),
        }
