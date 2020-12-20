from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	#Pages
	path('', views.home, name='home'),
	path('user/', views.userPage, name='user'),
	path('account/', views.accountSettings, name='account'),
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

	#Reset Password
	path('reset_password/', 
		auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), 
		name="reset_password"),
	path('reset_password_sent/', 
		auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
		name="password_reset_done"),
	#uidb: user id codif en base 64; token: token para chequear que el pass es válido 
	path('reset/<uidb64>/<token>/', 
		auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
		name="password_reset_confirm"),
	path('reset_password_complete/', 
		auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
		name="password_reset_complete"),
]