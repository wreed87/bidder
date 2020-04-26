from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import viewsets 
from users.serializers import CreateUserSerializer
from .models import Item, Auction
from .serializers import ItemsSerializer, AuctionsSerializer
from django.views.generic import TemplateView
import requests
import json


def registration(request):
    url = "http://193.61.36.119:8000/authentication/register/"
    data = {
        'username': request.POST.get("username", ""),
        'password': request.POST.get("password", "")
        }
    request = requests.post(url, data)
    return myapp_home(request)
    
    
#parent template page
class HomePageView(TemplateView):
    template_name = '_parent.html'
    
    
class ItemsViewList(viewsets.ModelViewSet):    
    queryset = Item.objects.all().order_by('itmTitle')    
    serializer_class = ItemsSerializer

class AuctionsViewList(viewsets.ModelViewSet):     
    queryset = Auction.objects.all()     
    serializer_class = AuctionsSerializer   



def myapp_signup(request): 
	return render(request,'signup.html',{})
    

def myapp_login(request): 
	return render(request,'login.html',{})


def myapp_home(request): 
   return render(request,'home.html',{})


def myapp_sell(request): 
    return render(request, 'sell.html',{})
       
        
def myapp_history(request):
    itemReading_url = "http://193.61.36.119:8000/v1/item/"
    token = 'zVtFi9wqoH6Zc9ANBdsKRu9m5VWnix'
    headers = {'Authorization': 'Bearer '+str(token)}
    response = requests.get(itemReading_url,headers=headers)
    itemList = []
    for i in range (len(response.json())):
        item = Item()
        item.itmTitle = response.json()[i].get('itmTitle')
        item.itmTimeStamp = response.json()[i].get('itmTimeStamp')
        item.itmIsNew = response.json()[i].get('itmIsNew')
        item.itmDescription = response.json()[i].get('itmDescription')    
        item.itmExpireDateTime = response.json()[i].get('itmExpireDateTime')    
        item.itmOwner = response.json()[i].get('itmOwner')
        itemList.append(item)
    return render(request, 'history.html',{'itemList': itemList}) 


def myapp_bid(request):
        return render(request,'bid.html',{})
