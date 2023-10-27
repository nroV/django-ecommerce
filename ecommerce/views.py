import os
import bcrypt
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from drf_yasg.utils import swagger_auto_schema

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from . serializers import *
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import *
from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
import stripe
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import *
from django.conf import settings
import random
from decimal import Decimal
# Create your views here.

# @api_view(['GET'])
# def getproduct(request,pk):
#     data:{}
#     query_set = Product.objects.all()
#     print(pk)
#     print(request.method)
#     print(request.GET.get('q'))

#     if query_set.exists():
#      serializer = ProductSerializer(    query_set,many=True)
#      return Response({
#         "message":    serializer.data
#      })

   
#     return Response({
#         "message":   'product not found'
#      })

class MyCustomPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    
    
    def get_paginated_response(self, data):
        return Response({
            'page_per_query': self.page_size,
            'page_size': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
class ProductListFilter(generics.ListAPIView,PageNumberPagination):
    serializer_class = ProductSerializerV2
    queryset = Product.objects.all()

    pagination_class = MyCustomPagination

  

   #  pagination_class

from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend
class ProductDiscount(generics.ListAPIView,PageNumberPagination):
    serializer_class = ProductSerializerV2
    queryset = Product.objects.all
    def get_queryset(self):
      #  print(self.kwargs['id'])
       queryset = Product.objects.filter( discount__gt=0)
       return queryset
       
class ProductListSort(generics.ListAPIView,PageNumberPagination):
    serializer_class = ProductSerializerV2
    queryset = Product.objects.all().order_by('-pk')
    filter_backends = [filters.SearchFilter]
    search_fields = ['productname']
   #  ordering_fields = ['price','productname']
    
    pagination_class = MyCustomPagination
    
    def get_queryset(self):
        print(super().get_queryset())
        price = self.request.GET.get('price', None)
        q =super().get_queryset()
        bestseller = self.request.GET.get('best_selling',None)
        popular = self.request.GET.get('popular',None)
        productname = self.request.GET.get('name',None)
        print(bestseller)
        
        if productname is not None :
           if productname.upper() =="DESC":
            q = Product.objects.all().order_by('-productname')
           else:
            q = Product.objects.all().order_by('productname')
        if bestseller is not None:
           if bestseller.upper() =="DESC":
            q = Product.objects.all().order_by('-sell_rating')
           else:
            q = Product.objects.all().order_by('sell_rating')
        #if none order = "ASC"

        if popular is not None:
              
           if popular.upper() =="DESC":
            q = Product.objects.all().order_by('-avg_rating')
           else:
            q = Product.objects.all().order_by('avg_rating')
        if price is not None:
         if  price.upper() == "DESC":
          q = Product.objects.all().order_by('-price')
    
         else :
          q = Product.objects.all().order_by('price')
      
        return q 
class ProductList(generics.ListAPIView,PageNumberPagination):
    serializer_class = ProductSerializerV2
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['price', 'category']
    search_fields = ['productname']
  
    pagination_class = MyCustomPagination
    def get_queryset(self):
    
      
        price = self.request.GET.get('prices', None)
        q =super().get_queryset()
        bestseller = self.request.GET.get('best_selling',None)
        popular = self.request.GET.get('popular',None)
        productname = self.request.GET.get('name',None)
  
        if productname is not None :
           if productname.upper() =="DESC":
            q = Product.objects.all().order_by('-productname')
           else:
            q = Product.objects.all().order_by('productname')
        if bestseller is not None:
           if bestseller.upper() =="DESC":
            q = Product.objects.all().order_by('-sell_rating')
           else:
            q = Product.objects.all().order_by('sell_rating')
        #if none order = "ASC"

        if popular is not None:
              
           if popular.upper() =="DESC":
            q = Product.objects.all().order_by('-avg_rating')
           else:
            q = Product.objects.all().order_by('avg_rating')
        if price is not None:
         if  price.upper() == "DESC":
          q = Product.objects.all().order_by('-price')
    
         else :
          q = Product.objects.all().order_by('price')
        print(bestseller)
        min_price = self.request.GET.get('min_price', None)
        max_price = self.request.GET.get('max_price', None)
    
        if min_price is not None and max_price is not None:
            q = self.queryset.filter(price__range=(min_price, max_price))

        return q 

   # #  pagination_class

   #  def get_queryset(self):
   #      print(super().get_queryset())
   #      q = get_list_or_404(Product)
   
   #      return   q 
class ProductRUD(generics.RetrieveUpdateDestroyAPIView)   :
   queryset = Product.objects.all() 
   # lookup_field = ['']
   # permission_classes = [IsAuthenticatedOrReadOnly]
   serializer_class = ProductSerializer
   def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        deleteproduct = Product.objects.get(pk = self.kwargs.get('pk',None))
        img = deleteproduct.imgid
      #   Images.objects.get(pk =img).delete()
      #   if deleteproduct.image:
      #    os.remove(deleteproduct.image.path)
        self.perform_destroy(instance)
        return Response({"status": "success", "code": status.HTTP_200_OK,
                        "message": "product has deleted successfully"}, status=status.HTTP_200_OK)


class ProductCreate(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductFavorite(generics.ListCreateAPIView):
   serializer_class = FavoriteSerializer
   queryset = Favorite.objects.all()
   def get_queryset(self):
      print(self.kwargs['pk'])
      try:
        user = get_object_or_404(Customer,pk = self.kwargs['pk'])
        q = Favorite.objects.filter(user = user)
        return q
      except Favorite.DoesNotExist:
       return Response(
           status=status.HTTP_400_BAD_REQUEST)
   def create(self, request, *args, **kwargs):
        pro = get_object_or_404(Product,pk = self.kwargs['pk'])
        fav = Favorite.objects.filter(products = pro)
      #   print(fav)
      #   print(pro)
        if fav.exists():
         print("It Exist")
           
         return Response({"status": "Product is in wishlist", 
                          "code": status.HTTP_201_CREATED,
                       }, status=status.HTTP_201_CREATED)
        else:
         pro = Product.objects.filter(pk =self.kwargs['pk'] )
         # print(self.request.data.get('user'))
         user = get_object_or_404(Customer,pk = self.request.data.get('user'))
      #check favorite
      
         try:
          try:
               oldfav = Favorite.objects.get(user = self.request.data.get('user'))
               # print(oldfav)
               prod = Product.objects.get(pk = self.kwargs['pk'] )
               print(prod)
               prod.isfavorite = True
               prod.save()
               oldfav.products.add(pro[0].pk)
               print('Here?')
               oldfav.save()
               return Response({"result": "success ", 
                          "code": status.HTTP_200_OK,
                       }, status=status.HTTP_200_OK)
          except Favorite.DoesNotExist:
               
    
       
           instance = favorite = Favorite.objects.create(
             user = user
           )
     
           
           for product in pro:
            print(product)
      
            prod = Product.objects.get(pk = product.pk )
            print(prod)
            prod.isfavorite = True
            prod.save()
            
            print(product.isfavorite)
            
     
            favorite.products.add(product.pk)
           
           favorite.save()
           return Response({"result": "success", 
                          "code": status.HTTP_200_OK,
                       }, status=status.HTTP_200_OK)
         
         except Favorite.DoesNotExist:
          oldfav = Favorite.objects.get(user = self.request.data.get('user'))
          instance = oldfav.save(products = pro,user = user )
      
          return Response({"result": instance, 
                          "code": status.HTTP_200_OK,
                       }, status=status.HTTP_200_OK)
  
   
   # def perform_create(self, serializer):
      
   #    pro = Product.objects.filter(pk =self.kwargs['pk'] )
   #    print(self.request.data.get('user'))
   #    user = get_object_or_404(Customer,pk = self.request.data.get('user'))
   #    #check favorite
      
   #    try:
   #       oldfav = Favorite.objects.get(user = self.request.data.get('user'))
   #       print(oldfav)
   #       oldfav.products.add(pro[0].pk)
       
   #       favorite = oldfav.save()
   #       return favorite
         
   #    except Favorite.DoesNotExist:
   #     instance = serializer.save(products = pro,user = user )
      
   #    return instance

class ProductFavoriteDestroy(generics.ListCreateAPIView):
   serializer_class = FavoriteSerializer
   queryset = Favorite.objects.all()

   def create(self, request, *args, **kwargs):
        pro = get_object_or_404(Product,pk = self.kwargs['pk'])
  
    
        fav = Favorite.objects.filter(products = pro)
      #   print(fav)
      #   print(pro)
        if fav.exists():
         oldfav = Favorite.objects.get(user = self.request.data.get('user'))
         d = oldfav.products.get(pk = self.kwargs['pk'])
         oldfav.products.remove(d)
         if(oldfav.products.count() == 0) :
            print("true")
            print(oldfav.products.count())
            oldfav.delete()
          
         else:
          pro.isfavorite = False
          pro.save()  
          instance = oldfav.save()
         
          print("Delete")
         
         
           
          return Response({"result": "Product has been deleted", 
                          "code": status.HTTP_201_CREATED,
                       }, status=status.HTTP_201_CREATED)
        else:
      
         return Response({"result": "not exist", 
                          "code": status.HTTP_404_NOT_FOUND,
                       }, status=status.HTTP_404_NOT_FOUND)
  
   
class ProductFavoriteCRUD(generics.RetrieveUpdateDestroyAPIView):
   serializer_class = FavoriteSerializer
   queryset = Favorite.objects.all()
   def update(self, request, *args, **kwargs):
      
      return super().update(request, *args, **kwargs)
   
   
class CategoryCreate(generics.CreateAPIView):
 serializer_class =CategorySerializerV2

class CategoryList(generics.ListAPIView):
   serializer_class = CategorySerializer
   queryset = Category.objects.all()
class CategoryRUD(generics.RetrieveUpdateDestroyAPIView,PageNumberPagination):
   serializer_class = CategorySerializer
   queryset = Category.objects.all()
  
   pagination_class = MyCustomPagination

   def destroy(self, request, *args, **kwargs):
      super().destroy(request, *args, **kwargs)
      return Response({"status": "success", "code": status.HTTP_200_OK,
                        "message": "category deleted successfully"}, status=status.HTTP_200_OK)

class OrderDetailCreate(generics.CreateAPIView):
   serializer_class =  OrderDetailSerializer

#    def perform_create(self, serializer):
#     print(self.request.data)
#     data = self.request.data
#     add = get_object_or_404(Address,pk =self.kwargs['pk'])
#         # Create the order
#    #  order = OrderDetail.objects.create(customer = serializer.validated_data['customer'])
#     total = 0
  
#     order = OrderDetail.objects.create(
#        customer = serializer.validated_data['customer'],  
#          amount = total,
#          address = add,
#          method = serializer.validated_data['method']
#          )

#         # Process each product
 
#     for product_data in data['products']:
#        product = Product.objects.get(id=product_data['id'])
#        quantity = product_data['quantity']


#             # Check if enough stock is available
#        if product.stockqty < quantity:
#                 return Response({"error": f"Not enough stock available for product {product.id}"})

#             # Create the OrderProduct
#          # Create the OrderProduct
#        OrderProduct.objects.create(order=order, product=product, quantity=quantity)
#        total +=   (quantity * product.price)
         

#         # Update the stock quantity of the product
#        product.stockqty -= quantity
#        #Increase product selling
#        product.sell_rating+= 1
#        product.save()
 
#       #  serializer = self.get_serializer(order)
#       #  return Response(serializer.data) 
#     print(f"total: {total}")  
  
#     order.amount = total
#     order.save()
  
#     send_mail(
#     f"Order {   order.id}",
#     """
#   Your order has been placed
#   thanks your for your order
# """,
#     "Nightpp19@gmail.com",
#      [ order.customer.email ],
#      fail_silently=False,
#    )
  
  

   def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
         print(self.request.data)
         data = self.request.data
         add = get_object_or_404(Address,pk =self.kwargs['pk'])
      
   
        # Create the order
   #  order = OrderDetail.objects.create(customer = serializer.validated_data['customer'])
         total = 0
  
         order = OrderDetail.objects.create(
           customer = serializer.validated_data['customer'],  
            amount = total,
         address = add,
         method = serializer.validated_data['method']
         )

        # Process each product
 
         for product_data in data['products']:
           product = Product.objects.get(id=product_data['id'])
           quantity = product_data['quantity']
           color = Colors.objects.get(id = product_data['colorselection'])
           size = Sizes.objects.get(id =product_data['size'])


            # Check if enough stock is available 
           if product.stockqty < quantity:
                return Response({"error": f"Not enough stock available for product {product.id}"})

            # Create the OrderProduct
         # Create the OrderProduct
         
         
           OrderProduct.objects.create(
                        order=order,
                                product=product,
                                quantity=quantity,
                                colorselection =color,
      
                                size = size
                                
                                
                                
                                )
           total +=   (quantity * product.price)
         

        # Update the stock quantity of the product
           product.stockqty -= quantity
       #Increase product selling
           product.sell_rating+= 1
           product.save()
 
      #  serializer = self.get_serializer(order)
      #  return Response(serializer.data) 
           print(f"total: {total}")  
   
         order.amount = total
         if(order.method.lower() == "online") :
            order.ispaid = True
         else:
            order.ispaid = False
         order.save()

#          send_mail(
#     f"Order {   order.id}",
#     """
#   Your order has been placed
#   thanks your for your order
# """,
#     "Nightpp19@gmail.com",
#      [ order.customer.email ],
#      fail_silently=False,
#    )
          
         return Response({
                "data": serializer.data,
                "id": order.id # Access the id of the created object
              }, status=status.HTTP_201_CREATED)
  
        
  
# def create(self, request, *args, **kwargs):
#     data = request.data
    
#     print("hello")
#     print(self.kwargs['pk'])

#     total = 0

#     # Calculate total and check stock before creating the order
#     for product_data in data['products']:
#         product = Product.objects.get(id=product_data['id'])
#         quantity = product_data['quantity']

#         # Check if enough stock is available
#         if product.stockqty < quantity:
#             return Response({"error": f"Not enough stock available for product {product.id}"})

#         total += quantity * product.price
#     add = get_object_or_404(Address,pk =kwargs.get('pk',None))
#     print(kwargs['pk'])
#     # Create the order
#     serializer = OrderDetailSerializer(data=request.data)
#     if serializer.is_valid():
#         order = OrderDetail.objects.create(
#             customer=serializer.validated_data['customer'],
#             amount=total,
#             address=add,
#             method=serializer.validated_data['method']
#         )

#         # Process each product
#         for product_data in data['products']:
#             product = Product.objects.get(id=product_data['id'])
#             quantity = product_data['quantity']

#             # Create the OrderProduct
#             OrderProduct.objects.create(order=order, product=product, quantity=quantity)

#             # Update the stock quantity of the product
#             product.stockqty -= quantity
#             # Increase product selling
#             product.sell_rating += 1
#             product.save()
#         order.amount = total
#         order.address =  get_object_or_404(Address,pk =kwargs.get('pk',None))
#         order.save()
#       #   send_mail(
#       #       f"Order {order.id}",
#       #       """
#       #       Your order has been placed
#       #       thanks your for your order
#       #       """,
#       #       "Nightpp19@gmail.com",
#       #       [order.customer.email],
#       #       fail_silently=False,
#       #   )

#         return Response({
#            "data": serializer.data,
#            "id": order.id
#         })

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailCreateV2(generics.CreateAPIView):
   serializer_class = OrderDetailSerializer
    
   def perform_create(self, serializer):
    print("hello")
    pk =  self.kwargs.get('pid',None)


    pro = Product.objects.get(pk = pk)
    pro.stockqty = pro.stockqty - serializer.validated_data['qty']
    total = pro.price * serializer.validated_data['qty']
    pro.save()

    obj = serializer.save(customer = serializer.validated_data['customer'],amount =    total,product =  pro )

    useremail = obj.customer.email


    instance = OrderDetail.objects.create(order_id = obj.id, customer = serializer.validated_data['customer'] )
    send_mail(
    f"Order {instance.order_id}",
    """
Your order has been placed
thanks your for your order
""",
    "Nightpp19@gmail.com",
     [ useremail ],
     fail_silently=False,
   )
     







class OrderDetailRetriandDelete(generics.GenericAPIView):
   def get(self,request,pk):
      order = get_object_or_404(OrderDetail,pk=pk)
      serializers = OrderDetailSerializer(order,many=False)
      return Response(serializers.data,status=HTTP_200_OK)

   def delete(self,request,pk):
     if pk is not None:
      serializers =  OrderDetailStatusSerializer(data=request.data)
      order = get_object_or_404(OrderDetail,pk=pk)
      if serializers.is_valid():
 
       order.delete()
       return Response({
          'message':'Order has deleted successfully',
          'success':'ok',
          'status':HTTP_200_OK
       },status=HTTP_200_OK)  
     else:
       return Response(serializers.errors,status=HTTP_400_BAD_REQUEST)  

      


@api_view(['PUT','DELETE'])     
def OrderStatus(request,pk):
   if request.method == 'PUT':

    if pk is not None:
     serializers =  OrderDetailStatusSerializer(data=request.data)
     order = get_object_or_404(OrderDetail,pk=pk)
    if serializers.is_valid():
   
       order.status = serializers.validated_data['status']

 
       if(order.method =="card") :
         pass
       else:
         if(serializers.validated_data['status'] =='Delivered'):
          order.ispaid = True
         else:
           order.ispaid = False
       order.save()
       return Response(serializers.data,status=HTTP_200_OK)  
    else:
       return Response(serializers.errors,status=HTTP_400_BAD_REQUEST)  


   else:
     return Response({
        "error":"please provide your parameter value"
     },status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])     

def finduser(request,pk):
   
   if request.method == "GET":
      if pk is not None :
      

          customer = get_object_or_404(Customer,pk = pk)
          serializers = CustomerSerializer(customer,many=False)
          
          return Response(serializers.data,HTTP_200_OK)
   
       
   
      
      else :
         return Response(
            {"message":"not found"},
            status=HTTP_400_BAD_REQUEST
         )
class OrderDetailView(generics.ListAPIView):
   serializer_class = OrderDetailSerializer
   queryset = OrderDetail.objects.all()
   
class OrderUserView(generics.ListAPIView):
   serializer_class = OrderDetailSerializer
   # pagination_class = None 
   queryset = OrderDetail.objects.all()
   def get_queryset(self):
    customer = get_object_or_404(Customer,pk = self.kwargs.get('pk',None) )
    print(customer)
    order = OrderDetail.objects.filter(customer=customer).order_by('-id')
    return order



      
   
class AddressList(generics.ListAPIView):
   queryset= Address.objects.all()
   serializer_class = AddressSerializer

class RetrieveCustomAddress(generics.ListAPIView):

   # def get(self,request,*arg,**kwargs):
   #    customer =get_object_or_404(Customer,pk=kwargs.get('pk',None))
   #    if customer is not None:
   #     addr = get_object_or_404(Address,customer_id=customer)
     
   #     serializers = AddressSerializer(addr)
   #       # Generate confirmation token and activation link
   #     confirmation_token = default_token_generator.make_token(user)
   #     activate_link_url = reverse('activate')
   #     activation_link = f'{activate_link_url}?user_id={user.id}&confirmation_token={confirmation_token}'

   #     return Response(serializers.data)
   #    else:
   #     return Response({
   #        "detail":"there is no related customer with by that id"
   #     },status=HTTP_404_NOT_FOUND)
  

   queryset= Address.objects.all()
   serializer_class = AddressSerializer
   def get_queryset(self):
      cus = get_object_or_404(Customer,pk = self.kwargs["pk"])
      q = Address.objects.filter(customer_id =cus)
      return q
class AddressFilter(generics.ListAPIView):
   
   queryset= Address.objects.all()
   serializer_class = AddressSerializer
   def get_queryset(self):
      cus = get_object_or_404(Customer,pk = self.kwargs["pk"])
      Address.objects.filter(customer_id =cus)
class AddressSingle(generics.RetrieveUpdateDestroyAPIView):
   queryset= Address.objects.all()
   serializer_class = AddressSerializer

   def destroy(self, request, *args, **kwargs):
      super().destroy(request, *args, **kwargs)
      return Response({"status": "success", "code": status.HTTP_200_OK,
                        "message": "Address has deleted successfully"}, status=status.HTTP_200_OK)


# class AddressUser(generics.RetrieveUpdateAPIView):
#    queryset= Address.objects.all()
#    serializer_class = AddressSerializer
#    # def get(self, request, *args, **kwargs):
  

#    #     pk = self.kwargs.get('pk',None)
#    #     print(pk)
#    #     if pk is not None:
#    #       pk =  self.kwargs.get('pid',None)
#    #       customer =Customer.objects.get(pk=pk)
#    #       print(customer)

#    #       return Address.objects.get(customer_id  =customer)
#    #     else:
#    #        return Response({
#    #           'response':'no detail'
#    #        })


   def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
       
       
class ReviewList(generics.ListCreateAPIView):
   queryset = ReviewRating.objects.all()
   serializer_class = ReviewSerializer


   def list(self, request, *args, **kwargs):
      # query = get_list_or_404(ReviewRating)
      query = ReviewRating.objects.all()
      if not query.exists():
       return Response({
          'message':'there is no data in the record'
       }) 
      return super().list(request, *args, **kwargs)  
   def perform_create(self, serializer):

      pro = get_object_or_404(Product,pk = self.request.data['product'])
      customer = get_object_or_404(Customer,pk =self.kwargs.get('pk',None) )
      print(self.kwargs.get('pk',None))
      oldreiview = ReviewRating.objects.filter(product =  self.request.data['product'] )&ReviewRating.objects .filter(customer =self.kwargs.get('pk',None))

      print(oldreiview)
      # ReviewRating.objects.filter(
      #    customer = self.kwargs.get('pk',None))
      if not oldreiview.exists() :


        if pro.avg_rating == 0:
         pro.avg_rating = serializer.validated_data['rating'] 

       
        else:
         pro.avg_rating =  (pro.avg_rating +  serializer.validated_data['rating'] )/2
        pro.save()  
        return serializer.save(product =pro,customer =  customer)
      else:
        theoldreview = ReviewRating.objects.get(product =  self.request.data['product'] )
        print(oldreiview)
        if pro.avg_rating == 0:
         pro.avg_rating = serializer.validated_data['rating'] 

       
        else:
         pro.avg_rating =  (pro.avg_rating +  serializer.validated_data['rating'] )/2
        pro.save() 
        
        theoldreview.product = pro
        theoldreview.customer = customer
        theoldreview.rating = serializer.validated_data['rating'] 
        theoldreview.description =  serializer.validated_data['description'] 
        theoldreview.save()
        return theoldreview.save()
      
      #   raise ValidationError({
      #      'message':'You cannot make a duplicate review only in 1 post'
      #   })



class ReviewProduct(generics.ListAPIView):
   queryset = ReviewRating.objects.all()
   serializer_class = ReviewSerializer
   
   def get_queryset(self):
       print(self.request.GET.get('pk',None))
       product = get_object_or_404(Product,pk = self.kwargs.get('pk',None))
       query = ReviewRating.objects.filter(product = product)
       return query
   
   
class ReviewRUD(generics.RetrieveUpdateDestroyAPIView):
   queryset = ReviewRating.objects.all()
   serializer_class = ReviewSerializer

   
   def destroy(self, request, *args, **kwargs):
      
       instance = super().destroy(request, *args, **kwargs)
       return Response(instance.data)
   def perform_update(self, serializer):
      instance = self.get_object()
      print(instance)
      #instance of the review before save
      updatedreview = serializer.save()
      pro = get_object_or_404(Product,pk = self.request.data['product'])

      if pro.avg_rating == 0:
         pro.avg_rating = serializer.validated_data['rating'] 
      else:
         pro.avg_rating = (    pro.avg_rating + serializer.validated_data['rating'] )/2

      pro.save()   
      return serializer.save(product = pro)   
      # return super().perform_update(serializer)
 
   # def perform_destroy(self, instance):
   #    # re = ReviewRating.objects.get(pk = self.kwargs['pk'])
   #    print(instance)
   #    # customer = Customer.objects.get(pk = self.request.data['customer'])
   #    # if  customer is not re.customer :
   #    #    raise ValidationError("You do not have permission")
   #    # else:
   #    return super().perform_destroy(instance)

class AddressCreate(generics.CreateAPIView):
   serializer_class = AddressSerializer
   def perform_create(self, serializer):
        # Perform additional actions before saving
        pk =  self.kwargs.get('pid',None)
        customer =get_object_or_404(Customer,pk = pk)
        print(pk)
        serializer.save(customer_id = customer  )
class ImageCreate(generics.ListCreateAPIView):
   serializer_class = ImageSerializer
   queryset = Images.objects.all()

   def generate_random_image_name(self, filename):
        random_number = random.randint(1000000, 9999999)
        extension = filename.split('.')[-1]
        new_filename = f'{random_number}.{extension}'
        return new_filename
     


   
   def get_queryset(self):
      instance =get_list_or_404(Images)
      return instance



   

   def create(self, request, *args, **kwargs):
      # print(request.FILES)
      img = request.FILES
      # print(img['images'].name)
      imgname = img['images'].name

      if img:
         img['images'].name = self.generate_random_image_name(imgname)

  

      instance = super().create(request, *args, **kwargs)
      print(instance.data['id'])

      return Response(
         {
            'success':'true',
            'message':'your image has been uploaded',
            'status':HTTP_200_OK,
            'url':instance.data
         },
         status=HTTP_200_OK
      )
     
class ImageRUD(generics.RetrieveAPIView):
   serializer_class = ImageSerializer
   queryset = Images.objects.all()
class ImageRUD(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ImageSerializer
  queryset = Images.objects.all()


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
verification_code = 0

@swagger_auto_schema(method='POST',request_body= CustomerSerializerResetPassword)
@api_view(['POST'])

def ResetPW(request):
 
   verification_code =random.randint(10000,50000)
   serializers = CustomerSerializerResetPassword(data=request.data)
   if serializers.is_valid():
      customer = Customer.objects.filter(email = serializers.validated_data['email']).first()
      PasswordResetCodes.objects.create(user = customer,code = verification_code)
      # pw.code =   verification_code
      if customer :
         # hash_pw = make_password(serializers.data['password'])
         # serializers.save(password = hash_pw)
         send_mail(
            'Reset Password',
            f'Please enter your verfication code to change your password thanks you bellow {verification_code }',
            'Nightpp19@gmail.com',
            [serializers.validated_data['email']],
            fail_silently=False,

        )
         return Response({
            "message":"Please verify an email that we have request"
         },status=HTTP_202_ACCEPTED)

      else:
         return Response({

         },status=HTTP_401_UNAUTHORIZED)   
   else:
      return Response(
         serializers.errors,
         status=HTTP_400_BAD_REQUEST
      )
 

@api_view(['POST'])
def VerifyCodePW(request):
   # serializers =  CustomerSerializerResetPassword(data=request.data)
   # if serializers.is_valid():

 email = request.data['email']
 customer = Customer.objects.filter(email = request.data['email']).first()

 if customer :
   pw = PasswordResetCodes.objects.get(user = customer)
   new_password = request.data['password']
   if str(pw.code)== str(request.data['code']) :
   
      #   code = request.data.get('code')
     
        user = Customer.objects.filter(email=email).first()
        pw.delete()
        if user :
           user.password = make_password( request.data['password'])
           user.save()
           return Response({
            "message":"Your password has reset successfully"
          },status=HTTP_202_ACCEPTED)

   else:
      return Response(
         serializers.errors,
         status=HTTP_400_BAD_REQUEST
      )  
    
   pass
 else :
  return Response({
             "message":"wrong user credential"
    },status=HTTP_401_UNAUTHORIZED)
  
  
@swagger_auto_schema(method='POST',request_body= CustomerSerializerLogin)
@api_view(['POST'])
def logincustomer(request):
    serializers =  CustomerSerializerLogin(data=request.data)
   #  print(request.data)

    if serializers.is_valid():       


        try:
         user = Customer.objects.get(email = serializers.validated_data['email'], is_activated = True)
         print(user.password)
         print(serializers.validated_data['password'])
         serialid = CustomerSerializerId (user,many=False)
         hashed_pwd = make_password(serializers.validated_data['password'])
         print(hashed_pwd)
       

         if check_password(request.data['password'],user.password) :

         
          refresh = RefreshToken.for_user( user )
          token = {
       'refresh': str(refresh),  
       'access': str(refresh.access_token),
       'user':serialid.data
          }
          return Response(token)
         else:
          return Response({
             "message":"wrong user credential"
          },status=HTTP_401_UNAUTHORIZED)
        except Customer.DoesNotExist:
          return Response({
             "data":"there is no user associated with consider register"
          },status=HTTP_401_UNAUTHORIZED)
      

       
    else:
       #validation error
       return Response(serializers.errors,status=HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='POST',request_body= CustomerSerializerV2)

@api_view(['POST'])
def socialauthregister(request):
  serializers = CustomerSerializerV2(data=request.data)
  print(request.data)
  if serializers.is_valid():
   text = serializers.validated_data["username"]
   arr = text.split(" ")
   print(arr[len(  arr )-1])
   thisfirstname = arr[0]
   thislastname = arr[1]
   thisusername = arr[len(  arr )-1]
   thispassword = make_password( serializers.validated_data["password"])
   serializers.save(username = thisusername,firstname = thisfirstname,
                    lastname = thislastname,telephone =  serializers.validated_data["telephone"],
                    password = thispassword
                     )
   newuser = Customer.objects.get(email = serializers.validated_data["email"])
   confirmation_token = default_token_generator.make_token(newuser)
   activate_link_url = reverse('activate')
   activation_link = f'{activate_link_url}?user_id={newuser.id}&confirmation_token={confirmation_token}'

        # Send email with activation link
   host = request.get_host()

   send_mail(
            'Activate your account',
            f'Please click on the following link to activate your account: {host}/{activation_link}>',
            'Nightpp19@gmail.com',
            [serializers.validated_data['email']],
            fail_silently=False,
      )
   
   #      refresh = RefreshToken.for_user(newuser)
   #      token = {
   #      'refresh': str(refresh),
   #      'access': str(refresh.access_token),
   #   }
      #   return Response(token)
       
   return Response( {
           "message":"An email has sent to your associated account"
        }, status=status.HTTP_201_CREATED)

    

  

     
#   I/flutter ( 6751): nightpp19@gmail.com
#   I/flutter ( 6751): 116512354859814328502
#   I/flutter ( 6751): SIV SOVANPANHAVORN (Vorni)  

  else:
   return Response(serializers.errors,status=HTTP_400_BAD_REQUEST) 

   pass



@swagger_auto_schema(method='POST',request_body= CustomerSerializerV3)

@api_view(['POST'])
def socialauthlogin(request):
  serializers = CustomerSerializerV3(data=request.data)
  print(request.data)
  if serializers.is_valid():
     
     try:
        customer = Customer.objects.get(email = serializers.validated_data['email'])
        print(customer)
     except Customer.DoesNotExist:
        return Response({
           "detail":"There are no email associate to that account"
        },status=HTTP_400_BAD_REQUEST)
   
   
     serialid = CustomerSerializerId (customer,many=False)
     refresh = RefreshToken.for_user( customer )
     token = {
       'refresh': str(refresh),  
       'access': str(refresh.access_token),
       'user':serialid.data
          }
  
     return Response( 
      
        token
           
        , status=status.HTTP_201_CREATED)

    

  

     
#   I/flutter ( 6751): nightpp19@gmail.com   userthis as email
#   I/flutter ( 6751): 116512354859814328502 usethisasspassword
#   I/flutter ( 6751): SIV SOVANPANHAVORN (Vorni)   

  else:
   return Response(serializers.errors,status=HTTP_400_BAD_REQUEST) 

   pass





@swagger_auto_schema(method='PUT', request_body= CustomerSerializerEdit)
@api_view(['PUT'])
def updateuserprofile(request,pk):
  try:
   user = Customer.objects.get(pk = pk )
   serializers =  CustomerSerializerEdit(   user ,data=request.data)
 

   if serializers.is_valid():       
         serializers.save()
         return Response( serializers.data ,status=HTTP_201_CREATED)
   else:
       #validation error
       return Response(serializers.errors,status=HTTP_400_BAD_REQUEST)  
  except Customer.DoesNotExist:
          return Response({
             "data":"there is no user associated with please create an account"
          },status=HTTP_400_BAD_REQUEST)
      



     
#   I/flutter ( 6751): nightpp19@gmail.com
#   I/flutter ( 6751): 116512354859814328502
#   I/flutter ( 6751): SIV SOVANPANHAVORN (Vorni)  






@swagger_auto_schema(method='POST',request_body= CustomerSerializer)
@api_view(['POST'])      
def register(request):
    print("register")

    serializers = CustomerSerializer(data=request.data)

    query_set = Customer.objects.filter(email = request.data['email'])
    if query_set.exists():
      return Response ({
                "error":"Email has already exist, try a new one"
             },status =HTTP_401_UNAUTHORIZED)
    if serializers.is_valid():
      olduser = Customer.objects.filter(email=serializers.validated_data['email'])
      print(olduser)
      if len(olduser) == 0:
             
        serializers.save()
        newuser = Customer.objects.get(email = serializers.validated_data['email'])
        hashed_password = make_password( newuser.password)
        
        newuser.password = hashed_password
    

        newuser.save()
  
        confirmation_token = default_token_generator.make_token(newuser)
        activate_link_url = reverse('activate')
        activation_link = f'{activate_link_url}?user_id={newuser.id}&confirmation_token={confirmation_token}'

        # Send email with activation link
        host = request.get_host()

        send_mail(
            'Activate your account',
            f'Please click on the following link to activate your account: {host}/{activation_link}>',
            'Nightpp19@gmail.com',
            [newuser.email],
            fail_silently=False,
      )
   
   #      refresh = RefreshToken.for_user(newuser)
   #      token = {
   #      'refresh': str(refresh),
   #      'access': str(refresh.access_token),
   #   }
      #   return Response(token)
       
        return Response( {
           "message":"An email has sent to your associated account"
        }, status=status.HTTP_201_CREATED)

    
  
  
  
      else:
             raise ValidationError({
                "error":"user already registered"
             })
    else:
     return Response(serializers.errors)
    
@api_view(['GET'])
def activate(request):
    user_id = request.GET.get('user_id')
    token = request.GET.get('confirmation_token')

    try:
        user = Customer.objects.get(pk=user_id)
        
        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid token"}, status=400)

        if user.is_activated:
            return Response({"error": "User is already active"}, status=400)
        user.is_activated = True
        user.is_active = True
        user.save()

        return Response({"message": "User activated successfully"}, status=200)

    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        return Response({"error": "Invalid link"}, status=400)
    