from concurrent.futures.process import _python_exit
from django.contrib import admin
from itertools import product
from random import choices
from unicodedata import decimal
from django.db import models
from django.conf import settings
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# many to many relationship
# Product - Promotion
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title= models.CharField(max_length=255)
    featured_product= models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='collections')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering= ['title']    

class Product(models.Model):
    title= models.CharField(max_length=255)
    slug = models.SlugField()
    description= models.TextField(null= True, blank =True)
    unit_price = models.DecimalField(max_digits=6,
    decimal_places=2, validators= [MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection= models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank = True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering= ['title']

class Customer(models.Model):
    MEMBERSHIP_BRONZE= 'B'
    MEMBERSHIP_SILVER= 'S'
    MEMBERSHIP_GOLD= 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    ]
    
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True,blank=True)
    membership = models.CharField(choices= MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE,max_length=255)
    user= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self) -> str:
         return f'{self.user.first_name} {self.user.last_name}'
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    @admin.display(ordering= 'user__last_name')
    def last_name(self):
        return self.user.last_name


    class Meta:
        ordering= ['user__first_name','user__last_name']
       
        
        
    

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_COMPLETE = 'C'
    ORDER_CHOICES = [
        (PAYMENT_STATUS_PENDING,'Pending'),
        (PAYMENT_STATUS_FAILED,'Failed'),
        (PAYMENT_STATUS_COMPLETE,'Complete')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status= models.CharField(max_length=1,choices=ORDER_CHOICES,default=PAYMENT_STATUS_PENDING)
    # we should never delete the orders because the represent our sales
    customer= models.ForeignKey(Customer,on_delete= models.PROTECT)

    class Meta:
        permissions= [
            ('cancel order','can cancel order')
        ]

   

#one to one relationship
class Address(models.Model):
    zip = models.CharField(default='-',max_length=5)
    street= models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)

class OrderItem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()    
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete= models.CASCADE,related_name= 'items')
    product= models.ForeignKey(Product,on_delete= models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators = [MinValueValidator(1)])


class Review(models.Model):    
    product= models.ForeignKey(Product,on_delete = models.CASCADE, related_name ='reviews')
    name= models.CharField(max_length=255)
    description= models.TextField()
    date= models.DateField(auto_now_add=True)
    
