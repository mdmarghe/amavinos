from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import slugify


class Customer(models.Model):
	id = models.BigAutoField(primary_key=True)
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name
	

	
	
class Category(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name


class Product(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	description=models.CharField(max_length=200,null=True, blank=True)
	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	

class Cata(Product):
	date=models.DateTimeField()
	duration=models.CharField(max_length=50, default='2 horas')
	location=models.CharField(max_length=50, default='Calle Antillano Campos, 5')
	slug = models.SlugField(unique=True)  # Campo per la slug

	def save(self, *args, **kwargs):
			# Genera la slug dal titolo e assegna al campo 'slug'
			self.slug = slugify(self.title)
			super(Cata, self).save(*args, **kwargs)



class Order(models.Model):
	id = models.BigAutoField(primary_key=True)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	id = models.BigAutoField(primary_key=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	id = models.BigAutoField(primary_key=True)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address