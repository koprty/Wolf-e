from django.shortcuts import get_object_or_404, render
from .models import Item, Review

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
