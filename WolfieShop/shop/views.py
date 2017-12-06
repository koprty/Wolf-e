from django.shortcuts import get_object_or_404, render, redirect
from .models import Item, Review, ShoppingCart, TransactionContents, TransactionOrder, Customer
from django import forms
from .forms import CustomerRegisterForm, LoginForm
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password

def index(request):
	books = Item.objects.filter(category='Books')
	stationery = Item.objects.filter(category='stationery')
	electronics = Item.objects.filter(category='Electronics')
	context = {
		'books' : books,
		'stationery' : stationery,
		'electronics' : electronics,
	}
	# check to see if there is a user logged in
	loggedIn(request)
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

#@transaction.commit_manually
def customer_register(request):
	if (request.method == "POST"):
		form = CustomerRegisterForm(request.POST)
		if form.is_valid():
			# We validate by checking the email
			# Get email to check if customer exists
			data = form.cleaned_data
			email = data['email']
			if customerExists(email):
				#customer already exists
				print ("CUSTOMER ALREADY EXISTS")
				context = {'form': form, 'error': "This email is unavailable for a new account."}
				return render(request, 'customerregister.html', context)
			else:
				firstname = data['firstname']
				lastname = data['lastname']
				phonenumber = data['phonenumber'] 
				passwordhash = data['passwordhash']
				query = "INSERT INTO wolfieshop_db.Customer(FirstName, LastName, Email, PhoneNumber, PasswordHash) \
				VALUES (" +  firstname + "," +  lastname + "," + email + "," + phonenumber + "," + passwordhash + ");" 
				#newCust = Customer(firstname=firstname, lastname=lastname, email=email, phonenumber=phonenumber, passwordhash=make_password(passwordhash))
				newCust = Customer(firstname=firstname, lastname=lastname, email=email, phonenumber=phonenumber, passwordhash=passwordhash)
				newCust.save()
				print (email+ " has been saved");
				return redirect("/")
			
		else:
			context = {'form': form, 'error': "Your form inputs were not valid, try again."}
	else:
		form = CustomerRegisterForm()
	context = {'form': form }
	return render(request, 'customerregister.html', context)


def customer_login(request):
	if (request.method == "POST"):
		form = LoginForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			email = data['email']
			passwordhash = data['passwordhash']
			#if (validateAccount(email, make_password(passwordhash))):
			if validateAccount(email, passwordhash):
				print ("This account is valid")
				request.session['username']= email
			else:
				form = LoginForm()
		else:
			form = LoginForm()
	context = {'form':form }

	return render(request, "customerlogin.html", context)

def logout(request):
	try:
		del request.session['username']
	except:
		pass
	context = { }
	return render(request, "logout.html", context)

# Helper functions:
def customerExists(email):
	query = "SELECT * FROM wolfieshop_db.Customer " \
			+ "WHERE Email='" + email + "';"
	customercontents = list(Customer.objects.raw(query))
	return len(customercontents) > 0

def validateAccount(email, password):
	# query = "SELECT * FROM wolfieshop_db.Customer " \
	# 		+ "WHERE Email='" + email + "' AND PasswordHash='" + password + "';"
	query = "SELECT * FROM wolfieshop_db.Customer " \
			+ "WHERE Email='" + email + "';"
	customercontents = list(Customer.objects.raw(query))
	for x in customercontents:
		print (x)

	return len(customercontents) > 0

# boolean function to check to see if someone has been logged in
def loggedIn(request):
	username = ""
	try:
		username = request.session['username']
		print ("Logged in")
	except KeyError as e:
		print ("Not Logged in")
		return False
	return True

# return the username of the user that is loggedin
def userlogged(request):
	username = None
	try:
  		username = request.session['username']
	except KeyError as e:
  		pass
	return username

