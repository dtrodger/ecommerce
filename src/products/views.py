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

from tags.models import Tag

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

	def get_initial(self):
		initial = super(ProductUpdateView, self).get_initial()
		tags = self.objects.all().tag_set.all()
		initial["tags"] = ", ".join([x.title for x in tags])
		return initial

	def form_valid(self, form):
		valid_data = super(ProductUpdateView, self).form_valid(form)
		tags = form.cleaned_data.get("tags")
		if tags:
			tag_list = tags.split(",")
			for tag in tag_list:
				new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
				new_tag.products.add(self.get_object())
		return valid_data


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
