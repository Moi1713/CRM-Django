from django.shortcuts import render
from django.http import HttpResponse

from accounts.models import Product, Customer, Order

from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

# Create your views here.

def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {"orders":orders, "customers":customers, "total_orders":total_orders, "total_customers":total_customers, "delivered":delivered, "pending":pending}

	return render(request, 'accounts/dashboard.html', context)

def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', { "products":products })

def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	order_count = orders.count()

	context = { 'customer':customer, "orders":orders, 'order_count':order_count }
	return render(request, 'accounts/customer.html', context)

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

class ViewPDF(View):
	def get(self, request, *args, **kwargs):
		products = Product.objects.all()

		pdf = render_to_pdf('reports/product_rep.html', {"products":products})
		return HttpResponse(pdf, content_type='application/pdf')

class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		products = Product.objects.all()
		
		pdf = render_to_pdf('reports/product_rep.html', {"products":products})

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "%s_List.pdf" %("Product")
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response