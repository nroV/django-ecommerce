import random
from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ['username', 'email']
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
       model = Images
       fields = [ 'id','images']
   

class CategorySerializerV2(serializers.ModelSerializer):
  
   class Meta:
      model = Category
      fields = ['id', 'categoryname']
class ProductSerializerV2(serializers.ModelSerializer):
    category =  CategorySerializerV2(many=False,read_only=False)
    owner = UserSerializer(many=False)
    class Meta:
      model = Product
      fields ='__all__'


class ReviewSerializer(serializers.ModelSerializer):
  
    class Meta:
      model = ReviewRating
      fields ='__all__'
      read_only_fields = ('avg_rating',)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
      model = Product
      fields ='__all__'


class CategorySerializer(serializers.ModelSerializer):
   product =  ProductSerializer(many=True,read_only=True)
   class Meta:
      model = Category
      fields = ['id', 'categoryname','product']

class OrderProductSerializer(serializers.ModelSerializer):
    
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']



class OrderDetailSerializer(serializers.ModelSerializer):

   products = OrderProductSerializer(source='orderproduct_set', many=True,read_only=True)


   class Meta:
      model =OrderDetail

      read_only_fields = ('amount','products',)

      fields = '__all__'

class OrderDetailStatusSerializer(serializers.ModelSerializer):
    
    class Meta:

      model =OrderDetail

      read_only_fields = ('customer','method','qty','amount','product',)

      fields = '__all__'



# class OrderSerializer(serializers.ModelSerializer):
#    class Meta:
#       model =Order
#       fields = '__all__'
class CustomerSerializerResetPassword(serializers.ModelSerializer):
  class Meta:
      model =Customer
      fields = ['email']
class CustomerSerializerLogin(serializers.ModelSerializer):
  class Meta:
      model =Customer
      fields = ['email','password']

class PasswordResetCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetCodes
        fields = ['user', 'code']
        
class CustomerSerializerV2(serializers.ModelSerializer):
  class Meta:
      model =Customer
      fields = ('username','email','password')

class CustomerSerializer(serializers.ModelSerializer):

   class Meta:
      model =Customer
      fields = '__all__'
      
class CustomerSerializerEdit(serializers.ModelSerializer):
   class Meta:
     model = Customer
     fields =('username','firstname','lastname','telephone')
  
class AddressSerializer(serializers.ModelSerializer):
   customer_id  = CustomerSerializer(many=False,read_only= True)
   class Meta:
      model =Address
      fields = '__all__'
 
