# myapp/urls.py This file is in the myapp folder!
from . import views
from django.urls import path

from .views import HomePageView

urlpatterns = [
	path('signup/', views.myapp_signup, name='myapp'),    
    path('_parent/', HomePageView.as_view(), name='_parent'),      
    path('', views.myapp_login, name='myapp'),
    path('home/', views.myapp_home, name='myapp'),
]

