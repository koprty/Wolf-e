from django.shortcuts import get_object_or_404, render
from .models import Item, Review, ShoppingCart, TransactionContents, TransactionOrder
from django import forms
from .forms import CustomerRegisterForm

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


def transaction_detail(request, transaction_id):
	transactionorder = get_object_or_404(TransactionOrder, transactionid = transaction_id)
	transactioncontents = get_transactioncontents(transaction_id)
	context = {
		'transactionorder' : transactionorder,
		'transactioncontents' : transactioncontents,
	}
	return render(request, 'transaction.html', context)

#get all transactioncontents rows with this transaction id. Should have unique item_ids within these rows.
def get_transactioncontents(transaction_id):
	query = "SELECT * FROM wolfieshop_db.TransactionContents " \
		+ "WHERE TransactionId=" + transaction_id + ";"
	transactioncontents = TransactionContents.objects.raw(query)
	return transactioncontents


def customer_register(request):
	if (request.method == "POST"):
		form = CustomerRegisterForm(request.POST)
		if form.is_valid():
			# do good stuff
			pass;
		else:
			print ("things are bad");
			#ideally post some error message
	else:
		print("this is not a post request...")
		form = CustomerRegisterForm()
	context = {'form': form}
	return render(request, 'customerregister.html', context)


def customer_login():
	context = {}
	return render(request, "customerlogin.html", context)

def admin_login():
	context = {}
	return render(request, "adminlogin.html", context)

