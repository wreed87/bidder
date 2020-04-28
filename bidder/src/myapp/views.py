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

#Global IP address to the server
URL_IP = "http://193.61.36.119:8000/"

#API call to register users
def registration(request):
    url = URL_IP + "authentication/register/"
    data = {
        'username': request.POST.get("username", ""),
        'password': request.POST.get("password", "")
        }
    requests.post(url, data)
    return myapp_login(request)
    
    
#Parent template page
class HomePageView(TemplateView):
    template_name = '_parent.html'


    
#Serializer viewLists    
class ItemsViewList(viewsets.ModelViewSet):    
    queryset = Item.objects.all().order_by('itmTitle')    
    serializer_class = ItemsSerializer

class AuctionsViewList(viewsets.ModelViewSet):     
    queryset = Auction.objects.all()     
    serializer_class = AuctionsSerializer   


#Basic methods to return pages when invoked.
def myapp_login(request): 
	return render(request,'login.html',{})

def myapp_login_home(request): 
   return render(request,'home.html',{'variable_login': True})
   
def myapp_signup(request): 
	return render(request,'signup.html',{})     
   
def myapp_home(request): 
   return render(request,'home.html',{'variable_default': True})
   
def myapp_sell(request): 
    return render(request, 'sell.html',{})
      
def myapp_history(request):
    return render(request, 'history.html') 
    
def myapp_bid(request):
    return render(request, 'bid.html') 
      

#API call to verify correct user login. Only accessible users will return login page    
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
    #Verifies if token exists enabling users to login
    if token != None:
        return render(request,'home.html',{'variable_login': True})
    #Returns page with 'Wrong Credentials' message, you can try again to login    
    return render(request,'login.html',{'variable_wrong_login': True})
    


#Method to view the list of all closed auctions for authorised users
#Method myapp_bid_table and myapp_history_table only differ at the return level. Future development will reduce this to one method only.   
def myapp_history_table(request):
    #verifies if user exists
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    token_url = URL_IP + "authentication/token/"
    token_data = {
        'username': username,
        'password': password
        }
    response = requests.post(token_url, token_data)    
    token = response.json().get('access_token')
    #if user is register and exists
    if token != None:
        #API call to obtain all auction details
        auction_url = URL_IP + "v1/auction/"        
        headers = {'Authorization': 'Bearer '+str(token)}
        response = requests.get(auction_url,headers=headers)
        bidList = []
        #loop across all available auctions
        for i in range (len(response.json())):
            #obtain their corresponding item that is been auction
            item = response.json()[i].get('itemID')
            item_url = URL_IP + "v1/item/"+ str(item)
            item_response = requests.get(item_url,headers=headers)
            multipleAuction = response.json()
            singleBid = multipleAuction[i]
            singleItem = item_response.json()
            #remove duplicate id attribute before merging collections
            singleItem.pop('id')
            singleBid.update(singleItem)
            #merge Item and Auction models into an array creating a unique bid collection to illustrate the details after.
            bidList.append(singleBid)
        #return full bid list of items to the history page
        return render(request, 'history.html',{'bidList':bidList})
    #if credential details failed, message will appear.
    return render(request,'home.html',{'variable_item_unsaved': True})



#Method to view the list of all open auctions for authorised users
#Method myapp_bid_table and myapp_history_table only differ at the return level. Future development will reduce this to one method only.
def myapp_bid_table(request):
    #verifies if user exists
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    token_url = URL_IP + "authentication/token/"
    token_data = {
        'username': username,
        'password': password
        }
    response = requests.post(token_url, token_data)    
    token = response.json().get('access_token')
    #if user is register and exists
    if token != None:
        #API call to obtain all auction details
        auction_url = URL_IP + "v1/auction/"        
        headers = {'Authorization': 'Bearer '+str(token)}
        response = requests.get(auction_url,headers=headers)
        bidList = []
        #loop across all available auctions
        for i in range (len(response.json())):
            #obtain their corresponding item that is been auction
            item = response.json()[i].get('itemID')
            item_url = URL_IP + "v1/item/"+ str(item)
            item_response = requests.get(item_url,headers=headers)
            multipleAuction = response.json()
            singleBid = multipleAuction[i]
            singleItem = item_response.json()
            #remove duplicate id attribute before merging collections
            singleItem.pop('id')
            singleBid.update(singleItem)
            #merge Item and Auction models into an array creating a unique bid collection to illustrate the details after.
            bidList.append(singleBid)    
            #return full bid list of items to bid page
        return render(request, 'bid.html',{'bidList':bidList,'bid_ready':True,'bid_post':True})        
    #if credential details failed, message will appear.
    return render(request,'home.html',{'variable_item_unsaved': True})
 


#Method to submit bids to open auctions for authorised users
def myapp_bidmade(request):
    #verifies if user exists
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    token_url = URL_IP + "authentication/token/"
    token_data = {
        'username': username,
        'password': password
        }
    response = requests.post(token_url, token_data)    
    token = response.json().get('access_token')
    #if user is register and exists
    if token != None:
        #API call to obtain all auction details
        auction_url = URL_IP + "v1/auction/" + request.POST.get("id", "") + "/"   
        headers = {'Authorization': 'Bearer '+str(token)}  
        auction_response = requests.get(auction_url,headers=headers)
        currentBid = auction_response.json().get('aucPrice')
        itemID = auction_response.json().get('itemID')
        newBid = request.POST.get("price", "")
        #API call to obtain all details for item related to the auction        
        item_url = URL_IP + "v1/item/" + str(itemID) + "/"
        item_response = requests.get(item_url,headers=headers)
        itemOwner = item_response.json().get('itmOwner')
        #verify if item owner is the same as biding user
        if itemOwner != username:
            #confirm if new bid is higher than current bid
            if newBid > currentBid:
                #update details with API patch call
                data = {
                        "aucPrice": newBid,
                        "aucBidder": username,
                        "aucWinner": username
                        }                
                response = requests.patch(auction_url,headers=headers,data=data)
                #if bid is higher, a congratulation message will appear.
                return render(request, 'bid.html',{'variable_won': True})  
            #if bid is lower than current bid, message will appear to say this
            return render(request, 'bid.html',{'variable_lost': True}) 
        #if item owner is bidding for its own item, a message will appear to prohibit this.
        return render(request, 'bid.html',{'variable_owner': True})     
    #if credential details failed, message will appear.
    return render(request,'home.html',{'variable_item_unsaved': True})
    

#Method to create an item for auctioning for authorised users
def start_auction (request):
    #verifies if user exists
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    token_url = URL_IP + "authentication/token/"
    token_data = {
        'username': username,
        'password': password
        }
    response = requests.post(token_url, token_data)    
    token = response.json().get('access_token')
    #if user is register and exists
    if token != None:
        item_url = URL_IP + "v1/item/"
        auction_url = URL_IP + "v1/auction/"
        headers = {'Authorization': 'Bearer '+str(token)}
        item_data = {
            "itmIsNew": request.POST.get("itmIsNew", ""),
            "itmTitle": request.POST.get("itmTitle", ""),    
            "itmTimeStamp": datetime.datetime.now(),
            "itmDescription": request.POST.get("itmDescription", "") ,
            "itmExpireDateTime": request.POST.get("itmExpireDateTime", ""),
            "itmOwner": username      
            }
        #API call to Create new item model based on the details submitted
        item_response = requests.post(item_url, headers=headers, data=item_data)
        itemID = item_response.json().get('id')
        auction_data = {
            "itemID": itemID,
            "aucPrice": "0.01",
            "aucBidder": "None",
            "aucIsOpen": True,
            "aucDateTimeCountdown": request.POST.get("itmExpireDateTime", ""),
            "aucWinner": "None"            
        }
        #API call to Create new auction model based on the details submitted
        auction_response = requests.post(auction_url, headers=headers, data=auction_data)
        #if confirmation message will appear to confirm item/auction was saved
        return render(request,'home.html',{'variable_item_saved': True})
    #if credential details failed, message will appear.
    return render(request,'home.html',{'variable_item_unsaved': True})
    
