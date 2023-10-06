from datetime import datetime

import os
from django.conf import settings
from django.db import models

# Create your models here.
from django.db import models
from rest_framework.validators import *
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class Images(models.Model):
    images = models.ImageField(upload_to="images", 
                                max_length=100, default=None, blank=False, null=False,
                                error_messages='image cannot be empty'
                                )
    
    def delete(self, *args, **kwargs):
        if os.path.isfile(self.images.path):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.images.path))
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return str(self.id)


class Customer(AbstractBaseUser,models.Model):
    username = None
    # since wwe extend from abstract base user we dont want to incluide username field again
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    firstname = models.CharField(max_length=25,null= False)
    lastname = models.CharField(max_length=25,null= False)
    username = models.CharField(max_length=40,null= False)
    email = models.EmailField(max_length=255,null= False,unique=False)
    password = models.CharField(max_length=255,null= False)
    telephone = PhoneNumberField(blank=True,null=True)
    isowner = models.BooleanField(default=False,null=True)
    last_login = models.DateTimeField(auto_now=True)
    is_activated = models.BooleanField(default=False)
    imgid = models.OneToOneField(Images,on_delete=models.CASCADE,null=True)
    gender = models.CharField(max_length=10,null= False)
    # created_at = models.DateTimeField(default=datetime.now())

    # owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)   

    def delete(self, *args, **kwargs):
        
        # for img in self.imgid.all():
        #     img.delete()  # This will also delete the image file
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.username+str(self.id )
class PasswordResetCodes(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    code = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return f'{self.user.username} - {self.code}'    



class Category(models.Model):
    categoryname = models.CharField(max_length=25,null=False,error_messages= "category cannot be empty")
    imgid = models.OneToOneField(Images,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.categoryname
    

class Colors(models.Model):
    color = models.CharField(max_length=25)
    desc = models.CharField(max_length=100,null=True,blank=True)


class Attributes(models.Model):
    size = models.CharField(max_length=25,null=True,blank=True)
    colorid = models.ManyToManyField(Colors,blank=True,null=True)
    weight = models.FloatField(null=True,blank=True)
    brand = models.CharField(max_length=25,null=True,blank=True)
    model = models.CharField(max_length=25,null=True,blank=True)
    material_name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.model+self.size+self.brand


class Product(models.Model):
   
    productname = models.CharField(max_length=25,null=False,error_messages= "product cannot be empty")
    price = models.FloatField(default=0)
    stockqty = models.IntegerField(default=0)
    category = models.ForeignKey(Category,on_delete= models.CASCADE,related_name= 'product')
    owner = models.ForeignKey(User,on_delete=models.CASCADE)    
    imgid = models.ManyToManyField(Images)
    avg_rating = models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)],default=0)
    discount = models.IntegerField(null=True,default=0)
    sell_rating = models.IntegerField(null=True,default=0)
    description  = models.CharField(null=False,default="This is a product description",max_length=100)
    attribution = models.ForeignKey(Attributes,on_delete= models.CASCADE,related_name= 'attribute',null=True,blank=True)
    # created_at = models.DateTimeField(default=datetime.now())
    def delete(self, *args, **kwargs):
        for img in self.imgid.all():
            img.delete()  # This will also delete the image file
        super().delete(*args, **kwargs)
    def __str__(self):
        return self.productname

class OrderDetail(models.Model):


    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    delivered = models.BooleanField(default=False)
    shipped_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now= True)
    method = models.CharField(max_length=20,null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    ispaid = models.BooleanField(default=False)
    status = models.CharField(max_length=20,default="Pending")
    products = models.ManyToManyField(Product, through='OrderProduct')



    def __str__(self) :
        return str(self.id)


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderDetail   , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

# class OrderDetail(models.Model):
#     created_date = models.DateTimeField(auto_now_add=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="customer")
#     # product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="product")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     qty = models.IntegerField()
#     method = models.CharField(max_length=20,null=False)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     ispaid = models.BooleanField(default=False)
#     status = models.CharField(max_length=20,default="Pending")
#     def __str__(self):
#         return str(self.id) + self.method +str(self. amount )+str(self.ispaid)
    
# class Order(models.Model):
#     order_id = models.IntegerField(null=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now= True)
    
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     delivered = models.BooleanField(default=False)
#     def __str__(self):
#         return str(self.order_id)+str(self.customer)
    



class Address(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="user_address")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)

    def __str__(self):
        return f"Address {self.id}"



class ReviewRating(models.Model):

    description = models.TextField()
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False,validators=[MinValueValidator(1),MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review Rating {self.id}"
class SuperDeal(models.Model):
    dealname = models.CharField(max_length=25,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    imgid = models.OneToOneField(Images,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f"SuperDeal {self.superdeal_id} for {self.product.name}"    