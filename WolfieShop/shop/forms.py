from .models import Customer, Review
from django import forms


class CustomerRegisterForm(forms.ModelForm):
	passwordhash = forms.CharField(widget=forms.PasswordInput, label="Password")
	class Meta:
		model = Customer
		fields =["firstname", "lastname", "email", "phonenumber", "passwordhash"]
		#exclude=("customerid")

class LoginForm(forms.ModelForm):
	passwordhash = forms.CharField(widget=forms.PasswordInput, label="Password")
	class Meta:
		model = Customer
		fields =["email", "passwordhash"]
		#exclude=("customerid")


class SubmitReviewForm(forms.ModelForm):
	rating = forms.ChoiceField(choices=[(x, x) for x in range(1, 6)])
	reviewtext = forms.CharField(widget=forms.Textarea, max_length=255, label="Leave a Review!")
	class Meta:
		model = Review
		fields=["rating", "reviewtext"]