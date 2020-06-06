from django.urls import path
from . import views

urlpatterns = [
	#Pages
	path('', views.home, name='home'),
	path('user/', views.userPage, name='user'),
	path('products/', views.products, name='products'),
	path('customer/<str:pk_test>/', views.customer, name='customer'),
	#Login/Register
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	#PDF
	path('pdf_view/<str:type>/', views.ViewPDF, name="pdf_view"),
	path('pdf_download/<str:type>/', views.DownloadPDF, name="pdf_download"),
	#CRUD
	path ('create_order/', views.createOrder, name="create_order"),
	path ('update_order/<str:pk>/', views.updateOrder, name="update_order"),
	path ('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

	path ('create_customer/', views.createCustomer, name="create_customer"),

	path ('create_product/', views.createProduct, name="create_product"),
]