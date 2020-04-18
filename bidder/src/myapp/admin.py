from django.contrib import admin
from .models import Item # Import Item class as model
from .models import Auction # Import Auction class as model

# Register your models here.

admin.site.register(Item) # Register the Item class in # admin
admin.site.register(Auction) # Register the Auction class in # admin
