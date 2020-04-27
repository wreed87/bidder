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
import requests, json, datetime

URL_IP = "http://193.61.36.119:8000/"

def registration(request):
    url = URL_IP + "authentication/register/"
    data = {
        'username': request.POST.get("username", ""),
        'password': request.POST.get("password", "")
        }
    requests.post(url, data)
    return myapp_login(request)
    
    
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
    
def verified_login(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    token_url = URL_IP + "authentication/token/"
    token_data = {
        'username': username,
        'password': password
        }
    response = requests.post(token_url, token_data) 
    token = response.json().get('access_token')
    if token != None:
        return render(request,'home.html',{'variable_login': True,'name':token})
    return render(request,'login.html',{})
    

def myapp_login(request): 
	return render(request,'login.html',{})


def myapp_login_home(request): 
   return render(request,'home.html',{'variable_login': True})
   
def myapp_home(request): 
   return render(request,'home.html',{'variable_default': True})
   
  
def myapp_sell(request): 
    return render(request, 'sell.html',{})
      
def myapp_history(request):
    return render(request, 'history.html') 
      
        
def myapp_history_table(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    token_url = URL_IP + "authentication/token/"
    token_data = {
        'username': username,
        'password': password
        }
    response = requests.post(token_url, token_data)    
    token = response.json().get('access_token')
    if token != None:
        itemReading_url = URL_IP + "v1/item/"
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
    return render(request,'home.html',{'variable_item_unsaved': True})


def myapp_bid(request):
        return render(request,'bid.html',{})


def start_auction (request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    token_url = URL_IP + "authentication/token/"
    token_data = {
        'username': username,
        'password': password
        }
    response = requests.post(token_url, token_data)    
    token = response.json().get('access_token')
    if token != None:
        item_url = URL_IP + "v1/item/"
        headers = {'Authorization': 'Bearer '+str(token)}
        item_data = {
            "itmIsNew": request.POST.get("itmIsNew", ""),
            "itmTitle": request.POST.get("itmTitle", ""),    
            "itmTimeStamp": datetime.datetime.now(),
            "itmDescription": request.POST.get("itmDescription", "") ,
            "itmExpireDateTime": request.POST.get("itmExpireDateTime", ""),
            "itmOwner": username      
            }
        requests.post(item_url, headers=headers, data=item_data)    
        return render(request,'home.html',{'variable_item_saved': True})
    return render(request,'home.html',{'variable_item_unsaved': True})
    
