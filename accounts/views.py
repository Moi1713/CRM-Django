from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user, allowed_users, admin_only

from accounts.models import *

from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from .forms import OrderForm, CustomerForm, ProductForm, CreateUserForm

# Create your views here.

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			group = Group.objects.get(name='customer')
			user.groups.add(group)
			Customer.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account created for ' + username)
			return redirect('login')

	return render(request, 'accounts/register.html', {'form':form})

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username or Password incorrect')
			return render(request, 'accounts/login.html')

	return render(request, 'accounts/login.html')

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = {'orders':orders, "total_orders":total_orders,
		"delivered":delivered, "pending":pending}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)

#Pages
@login_required(login_url='login')
@admin_only
def home(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Order created successfully')
			return redirect('/')

	orders = Order.objects.all()
	customers = Customer.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'form':form, "orders":orders, "customers":customers, "total_orders":total_orders, "total_customers":total_customers, "delivered":delivered, "pending":pending}

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', { "products":products })

@login_required(login_url='login')
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	order_count = orders.count()

	context = { 'customer':customer, "orders":orders, 'order_count':order_count }
	return render(request, 'accounts/customer.html', context)

#Generacion de Reportes
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

#Descarga de Reportes
@login_required(login_url='login')
def DownloadPDF(request, type):
	response = ViewPDF(request, type)
	filename = "%s_List.pdf" %("Product")
	content = "attachment; filename='%s'" %(filename)
	response['Content-Disposition'] = content
	return response

#Obtencion de datos y seleccion de plantilla para el reporte
def ViewPDF(request, type):
	if(type == 'products'):
		products = Product.objects.all()
		pdf = render_to_pdf('reports/product_rep.html', {"products":products})
		return HttpResponse(pdf, content_type='application/pdf')
	elif(type == 'orders'):
		pk_test = request.GET["customerID"]
		customer = Customer.objects.get(id=pk_test)
		orders = customer.order_set.all()
		order_count = orders.count()
		pdf = render_to_pdf('reports/orders_rep.html', {"orders":orders, "customer":customer, "order_count":order_count })
		return HttpResponse(pdf, content_type='application/pdf')

#CRUD operations

#Orders
@login_required(login_url='login')
def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	return render(request, 'accounts/order_form.html', {'form':form})

@login_required(login_url='login')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	return render(request, 'accounts/order_form.html', {"form":form})

@login_required(login_url='login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		messages.success(request, 'Order deleted successfully')
		return redirect('/')

	return render(request, 'accounts/delete.html', {'item':order})

#Customers
@login_required(login_url='login')
def createCustomer(request):
	form = CustomerForm()
	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	return render(request, 'accounts/customer_form.html', {'form':form})

@login_required(login_url='login')
def createProduct(request):
	form = ProductForm()
	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	return render(request, 'accounts/customer_form.html', {'form':form})