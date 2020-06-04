from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('products/', views.products, name='products'),
	path('customer/<str:pk_test>/', views.customer, name='customer'),
	path('pdf_view/<str:type>/', views.ViewPDF, name="pdf_view"),
	path('pdf_download/<str:type>/', views.DownloadPDF, name="pdf_download"),
]