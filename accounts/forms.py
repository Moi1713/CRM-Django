from django import forms
from django.forms import ModelForm
from .models import Order, Customer, Product

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

#Models
class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ('customer', 'product', 'status')
		widgets = {
			'customer' : forms.Select(attrs={'class':'form-control'}),
			'product' : forms.Select(attrs={'class':'form-control'}),
			'status' : forms.Select(attrs={'class':'form-control'}),
		}

class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']
		widgets = {
			'name' : forms.TextInput(attrs={'class': 'form-control'}),
			'phone' : forms.TextInput(attrs={'class': 'form-control'}),
			'email' : forms.TextInput(attrs={'class': 'form-control'}),
			'profile_pic' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
		}

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ('name', 'price', 'category', 'description', 'tags')
		widgets = {
			'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Product´s name'}),
			'price' : forms.TextInput(attrs={'class': 'form-control'}),
			'email' : forms.Textarea(attrs={'class': 'form-control'}),
			'category' : forms.Select(attrs={'class': 'form-control'}),
			'description' : forms.Textarea(attrs={'class': 'form-control'}),
			'tags' : forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
		}