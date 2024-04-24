from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from authService.forms.UserForm import CustomUserCreationForm, RegistrationForm
from django import template

register = template.Library()



class RegisterView(View):
    def get(self, request):
        # If the user is already authenticated, redirect them to the home page
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        form = RegistrationForm()
        return render(request, 'authService/auth/register.html', {'form': form})

    def post(self, request): 
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user, company = form.save()  # Save the new user object
            login(request, user)  # Log the user in
            return HttpResponseRedirect(reverse('home'))  # Redirect to a success page after registration
        else:
            print(form.errors)
            return render(request, 'authService/auth/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        # If the user is already authenticated, redirect them to the home page
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        form = CustomUserCreationForm()
        return render(request, 'authService/auth/login.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            print(form.errors)
            return render(request, 'authService/auth/login.html', {'form': form})