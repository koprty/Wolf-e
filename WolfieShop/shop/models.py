from django.db import models
from django.core.urlresolvers import reverse

class ShopItem(models.Model):
    itemid = models.AutoField(db_column='ItemId', primary_key=True)
    itemname = models.CharField(db_column='ItemName', max_length=100, blank=False, null=False)
    quantity = models.IntegerField(db_column='Quantity', blank=False, null=False)
    price = models.IntegerField(db_column='Price', blank=False, null=False)

    CATEGORIES = (
		('BOOKS', 'Books'),
		('STATIONERY', 'Stationary'),
		('ELECTRONICS', 'Electronics'),
	)
    category = models.CharField(
    	db_column='Category',
    	choices=CATEGORIES,
    	max_length=25,
    	blank=False,
    	null=False
    )
    
    rating = models.IntegerField(db_column='Rating', blank=True, null=True, default=0)
    numreviews = models.IntegerField(db_column='NumReviews', blank=False, null=False, default=0) 

    class Meta:
        db_table = 'shop_item'
