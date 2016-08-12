from django.shortcuts import render, get_object_or_404


class MultiSlugMixin(object):
	def get_object(self, *args, **kwargs):
		model = None
		slug = self.kwargs.get("slug")
		ModelClass = self.model
		
		if slug is not None:
			try:
				obj = get_object_or_404(ModelClass, slug=slug)
			except ModelClass.MultipleObjectsReturned:
				obj = ModelClass.objects.filter(slug=slug).order_by("-title").first()
		else:
			obj = super(MultiSlugMixin, self).get_object(*args, **kwargs)
		return obj
