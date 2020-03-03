# django-foxycart-form
An abstract Python form for use with Django and FoxyCart.  

## Directions:
Import this form into another forms.py file, and then make your custom form inherit from it.  Mark as readonly any fields that you want hmac validated.  All other fields will be marked as user-editable.

## Example Usage
### forms.py

	from wherever import FoxyCartForm

	class PurchaseForm(FoxyCartForm):
		pass
		# Add your custom fields or field replacements here.


### views.py

	from wherever import PurchaseForm
	
	purchase_form = PurchaseForm(
		foxycart_api_key=foxycart_api_key,
		initial={
			"code": "example",
			"name": "Example",
			"price": 199,
			"url": url,
			"quantity": 1,
		}
	)
	
### template.html

	<form method="post" action="">
			<table>
				{{ purchase_form.as_table }}
			</table>
			<input type="submit" value="Add to Cart" />
	</form>
