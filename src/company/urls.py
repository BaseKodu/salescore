from django.contrib import admin
from django.urls import path, include
from company import views

app_name = 'company'

urlpatterns = [
    path('', views.companyView.as_view(), name='home'),

]
