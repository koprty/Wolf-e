from .models import Customer, Review
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
		super(CustomerRegisterForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
			})