from django.db import models
from django.core.urlresolvers import reverse

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
    firstname = models.CharField(db_column='FirstName', max_length=20, verbose_name="First Name")
    lastname = models.CharField(db_column='LastName', max_length=20, verbose_name="Last Name")
    email = models.CharField(db_column='Email', max_length=30) 
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=15, blank=True, null=True, verbose_name="Phone Number")
    passwordhash = models.CharField(db_column='PasswordHash', max_length=100, verbose_name="Password")  

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


class ShoppingCart(models.Model):
    shoppingcartid = models.AutoField(db_column='ShoppingCartId', primary_key=True)
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CustomerId', blank=True, null=True)
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemId', blank=True, null=True)
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ShoppingCart'


class TransactionContents(models.Model):
    transactioncontentsid = models.AutoField(db_column='TransactionContentsId', primary_key=True)
    transactionid = models.IntegerField(db_column='TransactionId', blank=True, null=True)
    #we might not need customer id here
    customerid = models.IntegerField(db_column='CustomerId', blank=True, null=True)
    itemid = models.IntegerField(db_column='ItemId', blank=True, null=True)
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)
    priceperitem = models.IntegerField(db_column='PricePerItem', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TransactionContents'


class TransactionOrder(models.Model):
    transactionid = models.AutoField(db_column='TransactionId', primary_key=True)
    customerid = models.IntegerField(db_column='CustomerId', blank=True, null=True)
    totalprice = models.IntegerField(db_column='TotalPrice', blank=True, null=True)
    dateprocessed = models.DateTimeField(db_column='DateProcessed', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TransactionOrder'


class Shipment(models.Model):
    shipmentid = models.AutoField(db_column='ShipmentId', primary_key=True)
    transactionid = models.IntegerField(db_column='TransactionId', primary_key=False, null = True)
    provider = models.CharField(db_column='Provider', blank=True, max_length=20, null=False)
    shipmenttype = models.CharField(db_column='Type', blank=True, max_length=40, null=False, verbose_name="Type")
    address = models.CharField(db_column='Address', blank=True, max_length=200, null=False)
    fee = models.IntegerField(db_column='Fee', blank=True, null=True)

    #if they cancel transaction, then we should remove the shipment and payment out of the table
    class Meta:
        managed = False
        db_table = 'Shipment'

class Payment(models.Model):
    paymentid = models.AutoField(db_column='PaymentId', primary_key=True)
    transactionid = models.IntegerField(db_column='TransactionId', primary_key=False)
    paytype = models.CharField(db_column='Type', blank=True, max_length=10, null=False, verbose_name="Card Type")
    billingaddress = models.CharField(db_column='BillingAddress', max_length=200, blank=True, null=False, verbose_name="Billing Address")
    cardnum = models.CharField(db_column='CardNumber', blank=True, max_length=16, null=False, verbose_name="Card Number")
    cardexpire = models.CharField(db_column='CardExpiryDate', blank=True, max_length=5, null=False, verbose_name="Card Expiry Date")
    #if they cancel transaction, then we should remove the shipment and payment out of the table
    class Meta:
        managed = False
        db_table = 'Payment'


