from .models import Customer, Review, ShoppingCart, Shipment, Payment
from django import forms


class CustomerRegisterForm(forms.ModelForm):
	passwordhash = forms.CharField(widget=forms.PasswordInput, label="Password")
	class Meta:
		model = Customer
		fields =["firstname", "lastname", "email", "phonenumber", "passwordhash"]

	def __init__(self, *args, **kwargs):
		super(CustomerRegisterForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})

class LoginForm(forms.ModelForm):
	passwordhash = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")
	class Meta:
		model = Customer
		fields =["email", "passwordhash"]
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})

class SubmitReviewForm(forms.ModelForm):
	rating = forms.ChoiceField(choices=[(x, x) for x in range(1, 6)])
	reviewtext = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), max_length=255, label="Leave a Review!")
	class Meta:
		model = Review
		fields=["rating", "reviewtext"]
		
	def __init__(self, *args, **kwargs):
		super(SubmitReviewForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})

#add item to shopping cart
#https://stackoverflow.com/questions/2237064/passing-arguments-to-a-dynamic-form-in-django
#https://stackoverflow.com/questions/46137883/pass-extra-parameters-to-django-model-forms-along-with-request-post
class SubmitItemForm(forms.ModelForm):
	class Meta:
		model = ShoppingCart
		fields=["quantity"]
		
	def __init__(self, *args, **kwargs):
		quantinput = args[0]['quantity']
		super(SubmitItemForm, self).__init__(*args, **kwargs)
		self.fields['quantity'] = forms.ChoiceField(choices=[(x, x) for x in range(1, quantinput+1)])

# Add delivery and shipping information to DB
class ShipmentForm(forms.ModelForm):
	provider = forms.ChoiceField(choices=[(x,x) for x in ["UPS", "Wolfie Express", "USPS", "FedEx"]])
	shipmenttype = forms.ChoiceField(choices=[(x,x) for x in ["Standard 5-7 Day Shipping", "2 Day Rush Shipping", "1 Day Express Shipping"]])

	class Meta:
		model = Shipment
		fields = ['provider', 'shipmenttype', 'address']
	def __init__(self, *args, **kwargs):
		super(ShipmentForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})


class PaymentForm(forms.ModelForm):
	paytype = forms.ChoiceField(choices=["VISA", "American Express", "WolfieWallet"])
	class Meta:
		model = Payment
		fields = ['paytype', 'billingaddress', 'cardnum', 'cardexpire']
	def __init__(self, *args, **kwargs):
		super(PaymentForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})
