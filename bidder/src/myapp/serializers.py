from rest_framework import serializers
from .models import Item, Auction 

#Serialiazer for Item and Auction class model
class ItemsSerializer(serializers.ModelSerializer):   
   class Meta:      
       model = Item      
       fields = ('id','itmTitle','itmTimeStamp','itmIsNew','itmDescription','itmExpireDateTime','itmOwner')
       
class AuctionsSerializer(serializers.ModelSerializer):     
    class Meta:    
        model = Auction        
        fields = ('id','itemID','aucPrice','aucBidder','aucIsOpen','aucDateTimeCountdown','aucWinner')
        