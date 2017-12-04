from django.shortcuts import get_object_or_404, render
from .models import Item, Review, ShoppingCart

def index(request):
	books = Item.objects.filter(category='Books')
	stationery = Item.objects.filter(category='stationery')
	electronics = Item.objects.filter(category='Electronics')
	context = {
		'books' : books,
		'stationery' : stationery,
		'electronics' : electronics,
	}
	return render(request, 'index.html', context)

def item_detail(request, item_id):
	item = get_object_or_404(Item, itemid=item_id)
	reviews = get_reviews(item_id)
	
	context = {
		'item' : item,
		'reviews' : reviews,
	}
	return render(request, 'item.html', context)

def get_reviews(item_id):
	query = "SELECT * FROM wolfieshop_db.Review " \
		+ "WHERE ItemId=" + item_id + ";"
	reviews = Review.objects.raw(query)
	return reviews

def shoppingcart_detail(request, shoppingcart_id):
	shoppingcart = get_shoppingcart(shoppingcart_id)
	context = {
		'shoppingcart' : shoppingcart,
	}
	return render(request, 'shoppingcart.html', context)

#get all rows corresponding to the shoppingcart_id. THese rows should have the same shoppingcartid and
#customerid, but different items and corresponding quantities.
def get_shoppingcart(shoppingcart_id):
	query = "SELECT * FROM wolfieshop_db.ShoppingCart " \
		+ "WHERE ShoppingCartId=" + shoppingcart_id + ";"
	scrows = ShoppingCart.objects.raw(query)
	return scrows

#this method may be useful in the future to get the relevant shopping cart for a customer.
#Note that the table is set valued across certain fields, so multiple rows may be returned.
def get_shoppingcart_fromcust(customer_id):
	query = "SELECT * FROM wolfieshop_db.ShoppingCart " \
		+ "WHERE CustomerId=" + customer_id + ";"
	scrows = ShoppingCart.objects.raw(query)
	return scrows

#get all transactioncontents rows with this transaction id. Should have unique item_ids within these rows.
def get_transactioncontents(transaction_id):
	query = "SELECT * FROM wolfieshop_db.TransactionContents " \
		+ "WHERE TransactionId=" + transaction_id + ";"
	transactioncontents = TransactionContents.objects.raw(query)
	return transactioncontents

