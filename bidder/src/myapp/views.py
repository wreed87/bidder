from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import viewsets 
import requests

from users.serializers import CreateUserSerializer

from .models import Item, Auction
from .serializers import ItemsSerializer, AuctionsSerializer 

from django.views.generic import TemplateView

@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    CLIENT_ID = '773j9wwAm1JY2BXkISaJPuCuFF424qmusN4SVEI5'
    CLIENT_SECRET = '6pv3XObdO2BSOragugcvi7MQ1qtdADg38XHbYSquQY28JKhSHxTYdBPLcbjWr2KAtodLGcUYLTNG732Qx7oLOjpbINSQedZkRTpC0EHNyoVTxyjmaRXFMJlmrrQmKikl'
    IP_token = 'http://193.61.36.119:8000/o/token/'  
    IP_revoke_token ='http://193.61.36.119:8000/o/revoke_token/'
    
    '''
    Registers user to the server. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    # Put the data from the request into the serializer 
    serializer = CreateUserSerializer(data=request.data) 
    # Validate the data
    if serializer.is_valid():
        # If it is valid, save the data (creates a user).
        serializer.save() 
        # Then we get a token for the created user.
        # This could be done differentley 
        r = requests.post(IP_token, 
            data={
                'grant_type': 'password',
                'username': request.data['username'],
                'password': request.data['password'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        #return Response(r.json())
        #return render(request,'login.html',{})
        return home(request)
    return Response(serializer.errors)

def home(request):        
    return render(request, 'home.html',{})



# @api_view(['POST'])
# @permission_classes([AllowAny])
# def token(request):
    # '''
    # Gets tokens with username and password. Input should be in the format:
    # {"username": "username", "password": "1234abcd"}
    # '''
    # r = requests.post(
    # IP_token, 
        # data={
            # 'grant_type': 'password',
            # 'username': request.data['username'],
            # 'password': request.data['password'],
            # 'client_id': CLIENT_ID,
            # 'client_secret': CLIENT_SECRET,
        # },
    # )
    # return Response(r.json())



# @api_view(['POST'])
# @permission_classes([AllowAny])
# def refresh_token(request):
    # '''
    # Registers user to the server. Input should be in the format:
    # {"refresh_token": "<token>"}
    # '''
    # r = requests.post(
    # IP_token, 
        # data={
            # 'grant_type': 'refresh_token',
            # 'refresh_token': request.data['refresh_token'],
            # 'client_id': CLIENT_ID,
            # 'client_secret': CLIENT_SECRET,
        # },
    # )
    # return Response(r.json())


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def revoke_token(request):
    # '''
    # Method to revoke tokens.
    # {"token": "<token>"}
    # '''
    # r = requests.post(
        # IP_revoke_token, 
        # data={
            # 'token': request.data['token'],
            # 'client_id': CLIENT_ID,
            # 'client_secret': CLIENT_SECRET,
        # },
    # )
    # # If it goes well return sucess message (would be empty otherwise) 
    # if r.status_code == requests.codes.ok:
        # return Response({'message': 'token revoked'}, r.status_code)
    # # Return the error if it goes badly
    # return Response(r.json(), r.status_code)



# Create your views here.
def myapp_signup(request): #server takes a request
	return render(request,'signup.html',{})
    
def myapp_login(request): #server takes a request
	return render(request,'login.html',{})

def myapp_home(request): #server takes a request
    if request.user.is_authenticated():
        return render(request,'home.html',{})
    

#parent template page
class HomePageView(TemplateView):
    template_name = '_parent.html'
    
    
class ItemsViewList(viewsets.ModelViewSet):    
    queryset = Item.objects.all().order_by('itmTitle')    
    serializer_class = ItemsSerializer

class AuctionsViewList(viewsets.ModelViewSet):     
    queryset = Auction.objects.all()     
    serializer_class = AuctionsSerializer   
