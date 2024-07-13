from django.contrib import admin
from django.urls import path, include
from common import views


app_name = 'common'

urlpatterns = [
    path('', views.homeView.as_view(), name='home'),

]
