from django import forms

PUBLISH_CHOICES = (
	# ('',''),
	('publish', 'Publish'),
	('draft', 'Draft'),
	)

class ProductCreateForm(forms.Form):
	title = forms.CharField()
	description = forms.CharField(widget=forms.Textarea)
	price = forms.DecimalField()
	publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)

	def clean_price(self):
		price = self.cleaned_data.get("price")
		if price <= 1.00:
			raise forms.ValidationError("Price must be greater than 1")
		elif price >= 100:
			raise forms.ValidationError("Price must be less than 100")
		else:
			return price

	def clean_title(self):
		title = self.cleaned_data.get("title")
		if len(title) > 3:
			return title
		else:
			raise forms.ValidationError("Title must be grater than 3 characters long")
			raise forms.ValidationError("Price must be greater than 1")
