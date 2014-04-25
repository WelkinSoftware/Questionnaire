# Forms for screener pages
from django import forms
from django.forms.widgets import RadioSelect
from django.utils.safestring import mark_safe, SafeString

class RespondentIdentForm(forms.Form):
	error_css_class = 'error'
	required_css_class = 'required'
	firstName = forms.CharField(max_length=50, label='My first name is')
	middleName = forms.CharField(max_length=50,  required=False, label='My middle name is')
	lastName = forms.CharField(max_length=50, label='My last name is')
	birthDate = forms.DateField(label='My birth date is (mm/dd/yyyy)')
	contactPhone = forms.CharField( max_length=30, label='My phone number is')
	contactEmail = forms.EmailField( required=False, label='(optional) My e-mail address is')
