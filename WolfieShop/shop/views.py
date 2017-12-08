from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from .models import Item, Review, ShoppingCart, TransactionContents, TransactionOrder, Customer
from django import forms
from .forms import CustomerRegisterForm, LoginForm, SubmitReviewForm, SubmitItemForm
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password

"""
Home Page / Index
"""
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


"""
Item Details Page
"""
def item_detail(request, item_id):
	# Get item and reviews
	item = get_object_or_404(Item, itemid=item_id)
	reviews = get_reviews(item_id)
	
	form = None
	createreviewform = None
	additemform = None
	# Load review form
	if loggedIn(request):
		createreviewform = SubmitReviewForm()
		#print(item.quantity)
		#print(request.method)
		#print("request.POST:")
		#print(request.POST)
		data = request.POST.copy()
		data['quantity'] = item.quantity
		if item.quantity is None:
			data['quantity'] = 0#just make it 0 if they didn't input the quantity field, dropdown should give no options
		additemform = SubmitItemForm(data)
		#if form.is_valid():
		    #new_scrow.save()
		    #also update number of items in the item table, subtracting the quantity specified
	else:
		form = LoginForm()#fix this - doesn't work anymore, need more checking
	
	context = {
		'item' : item,
		'reviews' : reviews,
		'form' : form,
		'createreviewform' : createreviewform,
		'additemform' : additemform
	}
	return render(request, 'item.html', context)

def get_reviews(item_id):
	query = "SELECT * FROM wolfieshop_db.Review " \
		+ "WHERE ItemId=" + item_id + ";"
	reviews = Review.objects.raw(query)
	return reviews

def submit_review(request, item_id):
	if (request.method == "POST"):
		form = SubmitReviewForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			rating = data['rating']
			reviewtext = data['reviewtext']
			
			item = get_object_or_404(Item, itemid=item_id)
			
			customer_email = userlogged(request)
			customer = get_object_or_404(Customer, email=customer_email)

			new_review = Review(itemid=item, customerid=customer,rating=rating,reviewtext=reviewtext)
			new_review.save()
	
	return redirect("/item/" + item_id)
	
"""
Shopping Cart
"""
#editing to only display your shopping cart
def shoppingcart_detail(request):
	if not loggedIn(request):
		form = LoginForm()

	
	customer_email = userlogged(request)
	customer = get_object_or_404(Customer, email=customer_email)

	shoppingcart = get_list_or_404(ShoppingCart, customerid = customer)

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


"""
Customer Registration/Login
"""
def customer_register(request):
	if (loggedIn(request)):
		print("You don't need to register; you are already logged in as: {0}", userlogged(request))
		next = request.POST.get('next', '/')
		return redirect(next)
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
				if (phonenumber == None):
					phonenumber = ""
				passwordhash = data['passwordhash']
				query = "INSERT INTO wolfieshop_db.Customer(FirstName, LastName, Email, PhoneNumber, PasswordHash) \
				VALUES (" +  firstname + "," +  lastname + "," + email + "," + phonenumber + "," + passwordhash + ");" 
				#newCust = Customer(firstname=firstname, lastname=lastname, email=email, phonenumber=phonenumber, passwordhash=make_password(passwordhash))
				newCust = Customer(firstname=firstname, lastname=lastname, email=email, phonenumber=phonenumber, passwordhash=passwordhash)
				newCust.save()
				newSc = ShoppingCart(customerid=newCust)
				newSc.save()

				request.session['username']= email
				request.session['nam']= firstname

				print (email+ " has been saved");
				return redirect("/")
			
		else:
			context = {'form': form, 'error': "Your form inputs were not valid, try again."}
	else:
		form = CustomerRegisterForm()
	context = {'form': form }
	return render(request, 'customerregister.html', context)


def customer_login(request):
	if (loggedIn(request)):
		print("you are already logged in as:", userlogged(request))
		next = request.POST.get('next', '/')
		return redirect(next)

	if (request.method == "POST"):
		form = LoginForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			email = data['email']
			passwordhash = data['passwordhash']

			# if the email and password match an existing user
			if validateAccount(email, passwordhash):
				print ("This account is valid")
				request.session['username']= email
				request.session['nam']= getAccountName(email, passwordhash)

				# Redirect page to previous page
				next = request.POST.get('next', '/')
				return redirect(next)
			else:
				# if account is not valid, and password does not match, reload the form
				context = {'form':form, 'error': "Invalid username or password. Try again!" }
				form = LoginForm()
		else:
			context = {'form':form, 'error': "Invalid Form Data. Try again!" }
			form = LoginForm()
	else:
		form = LoginForm()
		context = {'form':form }
	return render(request, "customerlogin.html", context)

"""
Customer Logout
"""
def logout(request):
	try:
		del request.session['username']
		del	request.session['nam']
	except:
		pass
	context = { }
	return render(request, "logout.html", context)


#########################################################################################################
#################################### Helper functions ###################################################
#########################################################################################################
# check to see if a customer exists with the email given
def customerExists(email):
	query = "SELECT * FROM wolfieshop_db.Customer " \
			+ "WHERE Email='" + email + "';"
	customercontents = list(Customer.objects.raw(query))
	return len(customercontents) > 0

# check to correct login credentials
def validateAccount(email, password):
	query = "SELECT * FROM wolfieshop_db.Customer " \
			+ "WHERE Email='" + email + "' AND PasswordHash='" + password + "';"
	# query = "SELECT * FROM wolfieshop_db.Customer " \
	# 		+ "WHERE Email='" + email + "';"
	customercontents = list(Customer.objects.raw(query))
	return len(customercontents) > 0

def getAccountName(email, password):
	query = "SELECT CustomerId, FirstName as name FROM wolfieshop_db.Customer " \
			+ "WHERE Email='" + email + "' AND PasswordHash='" + password + "';"
	customercontents = list(Customer.objects.raw(query))
	print ("HELLO")
	print (customercontents[0].name)
	return customercontents[0].name

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
