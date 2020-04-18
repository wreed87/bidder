# myapp/urls.py This file is in the myapp folder!
from . import views
from django.urls import path

urlpatterns = [
	path('login/', views.myapp_login, name='myapp'),
]

