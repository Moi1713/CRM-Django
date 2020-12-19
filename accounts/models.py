from django.db import models
from django.contrib.auth.models import User

'''
#import para los signals
from django.db.models.signals import post_save
from django.dispatch import receiver

'''

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=50, null=True)
	email = models.EmailField(blank = True, null = True)
	profile_pic = models.ImageField(default="default.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
		('Indoor', 'Indoor'),
		('Outdoor', 'Outdoor'),
		)

	name = models.CharField(max_length=100)
	price = models.FloatField()
	category = models.CharField(max_length=50, null=True, blank=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name

class Order(models.Model):
	STATUS = (
		('Pending', 'Pending'),
		('Out for Delivery', 'Out for Delivery'),
		('Delivered', 'Delivered'),
		)

	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=100, null=True, choices=STATUS)

	def __str__(self):
		return self.product.name

'''
#Perfil de usuario asociado: ejemplo
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	first_name = models.CharField(max_lengh=200, null=True, blank=True)
	last_name = models.CharField(max_length=200, null=True, blank=True)
	phone = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.first_name

#forma 1: con decorator reciever
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		print('Profile created!')

#forma 2: 
def update_profile(sender, instance, created, **kwargs):
	if created == False:
		instance.profile.save()
		print('Profile updated')

post_save.connect(update_profile, sender=User)

'''