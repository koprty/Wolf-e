from .models import Customer
from django import forms


class CustomerRegisterForm(forms.ModelForm):
	passwordhash = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = Customer
		fields =["firstname", "lastname", "email", "phonenumber", "passwordhash"]
		#exclude=("customerid")

class LoginForm(forms.ModelForm):
	passwordhash = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = Customer
		fields =["email", "passwordhash"]
		#exclude=("customerid")
