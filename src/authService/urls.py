from django.contrib import admin
from django.urls import path, include
from authService import views

app_name = 'authService'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),

]
