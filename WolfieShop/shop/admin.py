from django.contrib import admin
from .models import Item, Customer, Review

# Register your models here.
admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(Review)
