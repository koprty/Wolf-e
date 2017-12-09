from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from .models import Item, Review, ShoppingCart, TransactionContents, TransactionOrder, Customer, Shipment, Payment
from django import forms
from .forms import CustomerRegisterForm, LoginForm, SubmitReviewForm, SubmitItemForm, ShipmentForm, PaymentForm
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password

SHIPPING_FEE = 3
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
	
	additemform = None
	createreviewform = None

	# Load Forms
	if loggedIn(request):
		data = request.POST.copy()
		
		data['quantity'] = item.quantity
		if item.quantity is None:
			data['quantity'] = 0#just make it 0 if they didn't input the quantity field, dropdown should give no options
		additemform = SubmitItemForm(data)

		if (request.method == "POST"):
			if additemform.is_valid() and 'additem' in request.POST:
				data = additemform.cleaned_data
				data['quantity'] = request.POST.get('quantity', False)
				quantity = data['quantity']
				
				item = get_object_or_404(Item, itemid=item_id)
			
				customer_email = userlogged(request)
				customer = get_object_or_404(Customer, email=customer_email)

				
				# Check if item exists in cart
				try:
					cart_item = ShoppingCart.objects.get(customerid=customer.customerid, itemid=item_id)
					if cart_item:
						print("Duplicate Item! Adding quantity to item in cart.")
						cart_item.quantity = cart_item.quantity + int(quantity)
						print("New quantity", cart_item.quantity)
						cart_item.save()
						return redirect("/shoppingcart")#todo: could just return to item page, and add context for success message
				except:
					pass
				
				# Otherwise, just add new item to cart
				new_scrow = ShoppingCart(itemid=item, customerid=customer,quantity=quantity)
				new_scrow.save()
	
				return redirect("/shoppingcart")#todo: could just return to item page, and add context for success message
	
		
			createreviewform = SubmitReviewForm(data)
			if createreviewform.is_valid() and 'submit_review' in request.POST:
				data = createreviewform.cleaned_data
				rating = data['rating']
				reviewtext = data['reviewtext']
				
				item = get_object_or_404(Item, itemid=item_id)
				
				customer_email = userlogged(request)
				customer = get_object_or_404(Customer, email=customer_email)
	
				new_review = Review(itemid=item, customerid=customer,rating=rating,reviewtext=reviewtext)
				new_review.save()
				
				return redirect("/item/" + item_id)	
		else:
			createreviewform = SubmitReviewForm()
			
	context = {
		'item' : item,
		'reviews' : reviews,
		'createreviewform' : createreviewform,
		'additemform' : additemform
	}
	
	return render(request, 'item.html', context)

def get_reviews(item_id):
	query = "SELECT * FROM wolfieshop_db.Review " \
		+ "WHERE ItemId=" + item_id + ";"
	reviews = Review.objects.raw(query)
	return reviews

"""
Shopping Cart
"""
#editing to only display your shopping cart
def shoppingcart_detail(request):
	shoppingcart = None
	if not loggedIn(request):
		form = LoginForm()
		context = {'shoppingcart': None, 'error': "Please login to view your shopping cart."}
	else:
		customer_email = userlogged(request)
		customer = get_object_or_404(Customer, email=customer_email)
		try:
			shoppingcart = get_list_or_404(ShoppingCart, customerid = customer)
			context = {'shoppingcart' : shoppingcart}
		except:
			context = {'shoppingcart': None, 'error': "Your Shopping Cart is empty. Visit item pages to add items."}
			return render(request, 'shoppingcart.html', context)

	return render(request, 'shoppingcart.html', context)

def checkout(request):
	return redirect("/shipping")

def shoppingcart_delete(request, customer_id, item_id):
	#delete the one with the appropriate itemid: https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models
	ShoppingCart.objects.filter(customerid = customer_id, itemid = item_id).delete()

	return redirect("/shoppingcart")



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

				request.session['username']= email
				request.session['nam']= firstname

				customer = get_object_or_404(Customer, email=email)
				request.session['customer']= customer.customerid

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
				customer = get_object_or_404(Customer, email=email)
				request.session['customer']= customer.customerid
				print(request.session['customer'])

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

""" 
Add Shipment - we get to this page only from the shopping cart page for now
"""
def add_shipping(request):
	if (loggedIn(request)):
		if (request.method == "POST"):
			currShip = getcurrentshipmentid
			currPay = getcurrentpaymentid
			if (currShip != None):
				# Display last shipment info
				#TODO FOR LATER
				request.session.ship = ""
				pass
			
			form = ShipmentForm(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				print (data)
				provider = data['provider']
				shipmenttype = data['shipmenttype']
				address = data['address']
				# We're going to be stupid and make the fee $3 for every transaction
				fee = SHIPPING_FEE
				newShipping = Shipment(provider=provider, shipmenttype=shipmenttype, address=address, fee=fee)
				newShipping.save()

				if (currShip == None):
					# Get rid of last shipment info placed and clear session
					# TODO actually delete the sql row please
					request.session.ship = ""
					pass
				# add the new shipping id into the cookies
				request.session['ship'] = newShipping.shipmentid

				print ("New Shipping id", request.session['ship'])

				context={}
				#proceed to the next step of the checkout flow
				return redirect("/payment")

			else:
				form = ShipmentForm()
				context = {'form':form, 'error': "Invalid Shipping Form Data. Try again!" }

		else:
			form = ShipmentForm()
			context = {'form':form , 'fee': SHIPPING_FEE}
	else:
		context = {'message': "Please log in to fill your cart and checkout"}
		next = request.POST.get('next', '/login')
		return redirect(next, context)

	return render(request, "add_delivery.html", context)

"""
Add payment
"""

class PaymentForm(forms.ModelForm):
	paytype = forms.ChoiceField(choices=[(x,x) for x in ["VISA", "American Express", "Wolfie Wallet"]])
	class Meta:
		model = Payment
		fields = ['paytype', 'billingaddress', 'cardnum', 'cardexpire']
	def __init__(self, *args, **kwargs):
		super(PaymentForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})


def add_payment(request):
	if (loggedIn(request)):
		if (request.method == "POST"):
			form = PaymentForm(request.POST)
			
			if form.is_valid():
				data = form.cleaned_data
				print (data)
				paytype = data['paytype']
				billingaddress = data['billingaddress']
				cardnum = data['cardnum']
				cardexpire = data['cardexpire']
				# We're going to be stupid and make the fee $3 for every transaction
				fee = SHIPPING_FEE
				newPayment = Payment(paytype=paytype, billingaddress=billingaddress, cardnum=cardnum, cardexpire=cardexpire)
				newPayment.save()

				# add the new payment id into the cookies
				request.session['pay'] = newPayment.paymentid
				print ("New payment id", request.session['pay'])

				#proceed to the last step of the checkout flow - confirm order
				return redirect("/confirm")

			else:
				form = PaymentForm()
				context = {'form':form, 'error': "Invalid Payment Form Data. Try again!" }

		else:
			form = PaymentForm()
			context = {'form':form , 'fee': SHIPPING_FEE}
	else:
		context = {'message': "Please log in to fill your cart and checkout."}
		next = request.POST.get('next', '/login')
		return redirect(next, context)

	return render(request, "add_payment.html", context)

def confirm_order(request):
	context = {}
	if (request.method == "POST"):
		return redirect("/done",context)
	else:
		currShip = getcurrentshipmentid
		if currShip == None:
			return redirect('/shipping',context)
		currPay = getcurrentpaymentid
		if currShip == None:
			return redirect('/payment',context)

		# display shopping cart
		customer_id = request.session['customer']
		shoppingcart = get_list_or_404(ShoppingCart, customerid = customer_id)

		# display shipping info
		shipp = Shipment.objects.get(shipmentid=getcurrentshipmentid(request))

		# display payment info
		payy = Payment.objects.get(paymentid=getcurrentpaymentid(request))

		context = {
			# 'provider': provider,
			# 'shipmenttype': shipmenttype,
			'shoppingcart': shoppingcart,
			'shipp':shipp,
			'payy':payy
			
		}


	return render(request, "confirm_order.html", context)

def processed_order(request):
	context = {}
	if (request.method == "POST"):
		return redirect("/",context)
	return render(request, "confirmed_order.html", context)	


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

# return the shipmentid
def getcurrentshipmentid(request):
	username = None
	try:
  		username = request.session['ship']
	except KeyError as e:
  		pass
	return username

# return the shipmentid
def getcurrentpaymentid(request):
	username = None
	try:
  		username = request.session['pay']
	except KeyError as e:
  		pass
	return username