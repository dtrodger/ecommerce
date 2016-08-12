from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

# Create your models here.

class Product(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField(blank=True)
	description = models.TextField(default="Default")
	price = models.DecimalField(max_digits=100, decimal_places=2, default = 9.99, null=True)
	sale_price = models.DecimalField(max_digits=100, decimal_places=2, default = 6.99, null=True, blank=True)
	def __unicode__(self):
		return self.title


def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.title)


pre_save.connect(product_pre_save_reciever, sender=Product)