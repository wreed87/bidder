from django.db import models
from datetime import datetime
from decimal import Decimal
from django.core.validators  import MinValueValidator
from django.utils import timezone

# Create your models here.


class Item(models.Model):
    itmTitle = models.CharField(max_length=60)
    itmTimeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    itmIsNew = models.BooleanField()
    itmDescription = models.CharField(max_length=100)
    itmExpireDateTime = models.DateTimeField(default=timezone.now)
    itmOwner = models.CharField(max_length=60)        

    
class Auction(models.Model):
    aucPrice = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))]) #ensures price is higher than 0
    aucBidder = models.CharField(max_length=60)
    aucIsOpen = models.BooleanField(default=True)
    aucDateTimeCountdown = models.DateTimeField()
    aucWinner = models.CharField(max_length=60)