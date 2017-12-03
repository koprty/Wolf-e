from django.contrib import admin
from .models import Item, Customer, Review#, ShoppingCart#, TransactionOrder, TransactionContents

# Register your models here.
admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(Review)
#admin.site.register(ShoppingCart)
#admin.site.register(TransactionOrder)
#admin.site.register(TransactionContents)
