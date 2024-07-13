from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from company.models import Company


User = get_user_model()

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data

    def get_user(self):
        return self.user

# forms.py


class UserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    company_name = forms.CharField(required=True, label='Law Firm')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'company_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('Enter a valid email address.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(list(e.messages))
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        company_name = cleaned_data.get('company_name')
        trading_name = cleaned_data.get('trading_name')

        if password and password2 and password != password2:
            raise forms.ValidationError({'password2': 'Passwords must match.'})


        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            company_name = self.cleaned_data['company_name']
            company = Company.objects.create(
                name=company_name,
            )
            user.companies.add(company, through_defaults={'access_level': UserTypeEnums.COMPANY_OWNER})
            Account.objects.create(
                name=f"{company.name}",
                account_type=AccountTypeEnums.TRUST,
                company=company
            )

        return user

