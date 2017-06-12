from django import forms

class UploadFileForm(forms.Form):
	w_character = forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '})
	myfile = forms.FileField(label='Attach Excel File')
	# from_col = forms.CharField(max_length=2, label='From Column (Ex: B)', widget=w_character)
	# to_col = forms.CharField(max_length=2, label='To Column (Ex: R)', widget=w_character)
	# from_row = forms.IntegerField(min_value=0, max_value=1048576, label='From Row (Ex: 32)')
	# to_row = forms.IntegerField(min_value=0, max_value=1048576, label='To Row (Ex: 273)')
	# header_row = forms.IntegerField(min_value=0, max_value=1048576, label='Header Row (Ex: 31)')

