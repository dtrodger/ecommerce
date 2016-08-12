from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Product
# Create your views here.

def detail_slug_view(request, slug=None):
	try:
		product = get_object_or_404(Product, slug=slug)
	except Product.MultipleObjectsReturned:
		product = Product.objects.filter(slug=slug).order_by("-title").first()
	template = "detail_view.html"
	context = {
		"product" : product
	}
	return render(request, template, context)

def detail_view(request, object_id=None):
	product = get_object_or_404(Product, id=object_id)
	template = "detail_view.html"
	context = {
		"product" : product
	}
	return render(request, template, context)


def list_view(request):
	print request.user
	queryset = Product.objects.all()
	template = "list_view.html"
	context = {
		"queryset" : queryset
	}
	return render(request, template, context)