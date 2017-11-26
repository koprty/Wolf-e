from django.shortcuts import render

from .models import Item

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
