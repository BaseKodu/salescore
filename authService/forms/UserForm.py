from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from company.models import Company

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    def save(self, *args, **kwargs) -> Any:
        company = kwargs.pop('company', None)
        if company:
            self.instance.company = company
        return super().save(*args, **kwargs)


class RegistrationForm(forms.ModelForm):

    email = forms.EmailField(label='Email', max_length=100)
    first_name = forms.CharField(label='First Name', max_length=100)
    password1 = forms.CharField(label='Password', max_length=100)
    password2 = forms.CharField(label='Password2', max_length=100)

    company_name = forms.CharField(label='Company Name', max_length=100)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'password1', 'password2', 'company_name']

    def save(self):
        #cleaned_data = super(RegistrationForm, self).clean()
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        password = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        company_name = self.cleaned_data['company_name']

        user = User.objects.filter(email=email).first()
        if user:
            raise forms.ValidationError("Email already exists. Please choose another one or login")
        elif password != password2:
            raise forms.ValidationError("Passwords don't match")
        else:   

            #create instances of company, user and address
            company = Company(name=company_name, trading_name=company_name)            
            user = User(username=email, email=email, first_name=first_name)
            
            "Create the company first in the database and then add the user to the company"
            user.set_password(password)
            company.save()
            user.save()
            user.company=company
            user.save()
            return user, company