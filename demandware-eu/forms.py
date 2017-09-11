from django import forms

class UploadFileForm(forms.Form):
	CHOICES = (
		('product_master', '1. Product Master',),
		('variant', '2. Variations',),
		('image', '3. Image',),
		('category', '4. Category',),
		('link', '5. Linking Categories-Products',),
		('related', '6. Related Products',),
	)
	w_character = forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '})
	data_type = forms.ChoiceField(widget=forms.Select, choices=CHOICES, label='Choise Data Type')
	myfile = forms.FileField(label='Attach Excel File')
	sheet_name = forms.CharField(label='Sheet Name', initial='data')
	header_row = forms.IntegerField(min_value=0, max_value=1048576, label='Header Row (Ex: 31)', initial=33)
	from_row = forms.IntegerField(min_value=0, max_value=1048576, label='From Row (Ex: 32)', initial=34)
	from_col = forms.CharField(max_length=2, label='From Column (Ex: B)', widget=w_character, initial='B')
	to_col = forms.CharField(max_length=2, label='To Column (Ex: R)', widget=w_character, initial='BV')
	to_row = forms.IntegerField(min_value=0, max_value=1048576, label='To Row (0 : import all)', initial=0)


class ExportForm(forms.Form):
	CHOICES = (
		(1, 'Catalogs Export',), 
		(2, 'Price Books Export',),
		(3, 'Inventory Lists Export',),
		(4, 'Category Export',), 
		(5, 'Product Export',), 
		(6, 'Recommend Export',), 
	)
	data_type = forms.ChoiceField(widget=forms.Select, choices=CHOICES, label='Choise Data Type')
