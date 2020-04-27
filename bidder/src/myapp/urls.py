# myapp/urls.py This file is in the myapp folder!
from . import views
from django.urls import path

from .views import HomePageView

urlpatterns = [
	path('signup/', views.myapp_signup, name='myapp_signup'),    
    path('_parent/', HomePageView.as_view(), name='_parent'),      
    path('', views.myapp_login, name='myapp_login'),
    path('authentication/registration/', views.registration, name='myapp_home'),    
    path('home/', views.myapp_home, name='myapp_home'),
	path('bid/', views.myapp_bid, name='myapp_bid'), 
	path('sell/', views.myapp_sell, name='myapp_sell'), 
	path('history/', views.myapp_history, name='myapp_history'),    
	path('historyverified/', views.myapp_history_table, name='myapp_history_table'), 
	path('submitItem/', views.start_auction, name='start_auction'),    
	path('verifiedlogin/', views.verified_login, name='verified_login'), 
]


