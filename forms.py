from django import forms
import hashlib
import hmac

def foxycart_field_name(product_code, field_name, field_value, api_key):
    field_name = field_name.replace(' ', '_').replace('.', '_')

    if isinstance(field_name, str) or isinstance(field_name, unicode):
        field_name = escape(field_name)

    # For the hashed portion, only escape ampersands
    field_value_amp_only = str(field_value).replace('&', '&amp;')

    digest = hmac.new(
        api_key.encode('utf-8'),
        msg=('%s%s%s' % (
            product_code,
            field_name,
            field_value_amp_only,
        )).encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    if field_value == '--OPEN--':
        digest += '||open'

    return '%s||%s' % (field_name, digest)

class FoxyCartForm(forms.Form):

	def __init__(self, foxycart_api_key, *args, **kwargs):
		super(FoxyCartForm, self).__init__(*args, **kwargs)

		if 'code' in kwargs['initial']:
			code = kwargs['initial']['code']
		elif 'code' in self.fields:
			code = self.fields['code'].initial
		else:
			raise NameError()

		fields = collections.OrderedDict()
		for key, field in self.fields.items():
			initial = ""
			name = key

			if key in kwargs['initial']:
				initial = kwargs['initial'][key]
			elif field.initial:
				initial = field.initial

			readonly = False
			if 'readonly' in field.widget.attrs and field.widget.attrs['readonly']:
				readonly = True

			if readonly:
				name = foxycart_field_name(code, key, initial, foxycart_api_key)
				field.initial = initial
			else:
				name = foxycart_field_name(code, key, "--OPEN--", foxycart_api_key)

			fields[name] = field
		self.fields = fields

	name = forms.CharField(required=True, widget = forms.HiddenInput(attrs={"readonly": True}))
	code = forms.CharField(required=True, widget = forms.HiddenInput(attrs={"readonly": True}))
	price = forms.DecimalField(required=True, widget = forms.HiddenInput(attrs={"readonly": True}))
	image = forms.URLField(required=False, widget = forms.HiddenInput(attrs={"readonly": True}))
	url = forms.URLField(required=False, widget = forms.HiddenInput(attrs={"readonly": True}))
	quantity = forms.IntegerField(required=True, widget = forms.HiddenInput(attrs={"readonly": True}))
	quantity_min = forms.IntegerField(required=False, initial=1, widget = forms.HiddenInput(attrs={"readonly": True}))
	quantity_max = forms.IntegerField(required=False, widget = forms.HiddenInput(attrs={"readonly": True}))
