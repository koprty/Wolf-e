from django.db import models
from django.urls import reverse


class Item(models.Model):
    itemid = models.AutoField(db_column='ItemId', primary_key=True)
    itemname = models.CharField(db_column='ItemName', max_length=100, blank=False, null=False)
    quantity = models.IntegerField(db_column='Quantity', blank=False, null=False)
    price = models.DecimalField(max_digits=10,decimal_places=2,db_column='Price', blank=False, null=False)

    CATEGORIES = (
		('BOOKS', 'Books'),
		('STATIONERY', 'Stationery'),
		('ELECTRONICS', 'Electronics'),
	)
    category = models.CharField(
    	db_column='Category',
    	choices=CATEGORIES,
    	max_length=25,
    	blank=False,
    	null=False
    )
    
    rating = models.DecimalField(max_digits=3,decimal_places=2,db_column='Rating', blank=True, null=True, default=0)
    numreviews = models.IntegerField(db_column='NumReviews', blank=False, null=False, default=0) 

    class Meta:
        managed = False
        db_table = 'Item'

class Customer(models.Model):
    customerid = models.AutoField(db_column='CustomerId', primary_key=True)
    firstname = models.CharField(db_column='FirstName', max_length=20)
    lastname = models.CharField(db_column='LastName', max_length=20)
    email = models.CharField(db_column='Email', max_length=30) 
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customer'

class Review(models.Model):
    reviewid = models.AutoField(db_column='ReviewId', primary_key=True)
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemId')
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CustomerId')
    rating = models.IntegerField(db_column='Rating')
    reviewtext = models.CharField(db_column='ReviewText', max_length=255, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'Review'
        unique_together = (('itemid', 'customerid'),)


class ShoppingCart(models.Model):
    shoppingcartid = models.IntegerField(db_column='ShoppingCartId', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CustomerId', blank=True, null=True)  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemId', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ShoppingCart'
