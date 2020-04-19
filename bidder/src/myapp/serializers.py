from rest_framework import serializers
from .models import Item, Auction 


class ItemsSerializer(serializers.ModelSerializer):   
   class Meta:      
       model = Item      
       fields = ('itmTitle','itmTimeStamp','itmIsNew','itmDescription','itmExpireDateTime','itmOwner')
       
class AuctionsSerializer(serializers.ModelSerializer):     
    class Meta:    
        model = Auction        
        fields = ('aucPrice','aucBidder','aucIsOpen','aucDateTimeCountdown','aucWinner')
        