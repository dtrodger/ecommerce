import os

from mimetypes import guess_type

from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from digitalmarket.mixins import (
	LoginRequiredMixin,
	SubmitBtnMixin
	)

from .mixins import ProductManagerMixin
from .models import Product
from .forms import ProductModelForm


class ProductCreateView(SubmitBtnMixin, LoginRequiredMixin, CreateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	submit_btn = "Add Product"

	def form_valid(self, form):
		user = self.request.user
		form.instance.user = user
		valid_data = super(ProductCreateView, self).form_valid(form)
		form.instance.managers.add(user)
		return valid_data


class ProductUpdateView(SubmitBtnMixin, ProductManagerMixin, UpdateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	submit_btn = "Update Product"


class ProductDetailView(DetailView):
	model = Product


class ProductDownloadView(DetailView):
	model = Product

	def get(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj in request.user.myproducts.products.all():
			filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
			guessed_type = guess_type(filepath)[0]
			wrapper = FileWrapper(file(filepath))
			mimetype = 'application/force-download'
			if guessed_type:
				mimetype = guessed_type
			response = HttpResponse(wrapper, content_type=mimetype)

			if not request.GET.get("preview"):
				response["Content-Disposition"] = "attachment; filename=%s" %(obj.media.name)
			response["X-SendFile"] = str(obj.media.name)
			return response
		else:
			raise Http404


class ProductListView(ListView):
	model = Product

	#Ecommerce 2 for advanced query
	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(**kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
				Q(title__icontains=query)|
				Q(description__icontains=query)
			).order_by("-title")
		return qs



# def create_view(request):
# 	form = ProductModelForm(request.POST or None)
# 	if form.is_valid():
# 		#form.save()
# 		instance = form.save(commit=False)
# 		instance.sale_price = instance.price
# 		instance.save()
		
# 	# if form.is_valid():
# 	# 	data = form.cleaned_data
# 	# 	title = data.get("title")
# 	# 	description = data.get("description")
# 	# 	price = data.get("price")
# 	# 	new_obj = Product.objects.create(title=title, description=description, price=price)
	
# 	template = "form.html"
# 	context = {
# 		"form" : form,
# 		"submit_btn" : "Create Product",
# 	}
# 	return render(request, template, context)

# def update_view(request, object_id=None):
# 	product = get_object_or_404(Product, id=object_id)
# 	form = ProductModelForm(request.POST or None, instance=product)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.save()
# 	template = "form.html"
# 	context = {
# 		"product" : product,
# 		"form" : form,
# 		"submit_btn" : "Update Product",
# 	}
# 	return render(request, template, context)

# def detail_slug_view(request, slug=None):
# 	try:
# 		product = get_object_or_404(Product, slug=slug)
# 	except Product.MultipleObjectsReturned:
# 		product = Product.objects.filter(slug=slug).order_by("-title").first()
# 	template = "detail_view.html"
# 	context = {
# 		"product" : product
# 	}
# 	return render(request, template, context)

# def detail_view(request, object_id=None):
# 	product = get_object_or_404(Product, id=object_id)
# 	template = "detail_view.html"
# 	context = {
# 		"product" : product
# 	}
# 	return render(request, template, context)


# def list_view(request):
# 	print request.user
# 	products = Product.objects.all()
# 	template = "list_view.html"
# 	context = {
# 		"products" : products
# 	}
# 	return render(request, template, context)