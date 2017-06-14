from django import forms

class UploadFileForm(forms.Form):
	w_character = forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '})
	myfile = forms.FileField(label='Attach Excel File')
	from_row = forms.IntegerField(min_value=0, max_value=1048576, label='From Row (Ex: 32)', initial=15)
	from_col = forms.CharField(max_length=2, label='From Column (Ex: B)', widget=w_character, initial='B')
	to_col = forms.CharField(max_length=2, label='To Column (Ex: R)', widget=w_character, initial='C')
	to_row = forms.IntegerField(min_value=0, max_value=1048576, label='To Row (0 : import all)', initial=0)
	header_row = forms.IntegerField(min_value=0, max_value=1048576, label='Header Row (Ex: 31)', initial=14)
