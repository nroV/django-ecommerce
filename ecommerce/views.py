import os
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
    page_size = 1
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
       queryset = Product.objects.filter( discount__gt=0)
       return queryset
       
class ProductListSort(generics.ListAPIView,PageNumberPagination):
    serializer_class = ProductSerializerV2
    queryset = Product.objects.all().order_by('-price')
   #  filter_backends = [DjangoFilterBackend,OrderingFilter]
   #  ordering_fields = ['price','productname']
    pagination_class = MyCustomPagination
    
    def get_queryset(self):
        print(super().get_queryset())
        price = self.request.GET.get('price', None)
        q =super().get_queryset()
        bestseller = self.request.GET.get('best_selling',None)
        popular = self.request.GET.get('popular',None)

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
        min_price = self.request.GET.get('min_price', None)
        max_price = self.request.GET.get('max_price', None)

        if min_price is not None and max_price is not None:
            self.queryset = self.queryset.filter(price__range=(min_price, max_price))

        return self.queryset

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



class CategoryCreate(generics.CreateAPIView):
 serializer_class =CategorySerializerV2

class CategoryList(generics.ListAPIView):
   serializer_class = CategorySerializer
   queryset = Category.objects.all()
class CategoryRUD(generics.RetrieveUpdateDestroyAPIView):
   serializer_class = CategorySerializer
   queryset = Category.objects.all()

   def destroy(self, request, *args, **kwargs):
      super().destroy(request, *args, **kwargs)
      return Response({"status": "success", "code": status.HTTP_200_OK,
                        "message": "category deleted successfully"}, status=status.HTTP_200_OK)

class OrderDetailCreate(generics.CreateAPIView):
   serializer_class =  OrderDetailSerializer
    
   def perform_create(self, serializer):
    print(self.request.data)
    data = self.request.data

        # Create the order
   #  order = OrderDetail.objects.create(customer = serializer.validated_data['customer'])
    total = 0
    order = OrderDetail.objects.create(
       customer = serializer.validated_data['customer'],  
         amount = total
         )

        # Process each product
    for product_data in data['products']:
       product = Product.objects.get(id=product_data['id'])
       quantity = product_data['quantity']

       # 5


       #3 

            # Check if enough stock is available
       if product.stockqty < quantity:
                return Response({"error": f"Not enough stock available for product {product.id}"})

            # Create the OrderProduct
         # Create the OrderProduct
       OrderProduct.objects.create(order=order, product=product, quantity=quantity)
       total +=   (quantity * product.price)
         

        # Update the stock quantity of the product
       product.stockqty -= quantity
       #Increase product selling
       product.sell_rating+= 1
       product.save()
 
      #  serializer = self.get_serializer(order)
      #  return Response(serializer.data) 
    order.amount = total
    order.save()
  
    send_mail(
    f"Order {   order.id}",
    """
  Your order has been placed
  thanks your for your order
""",
    "Nightpp19@gmail.com",
     [ order.customer.email ],
     fail_silently=False,
   )
    return Response(serializer.data)  


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



class OrderDetailView(generics.ListAPIView):
   serializer_class = OrderDetailSerializer
   queryset = OrderDetail.objects.all()
class AddressList(generics.ListAPIView):
   queryset= Address.objects.all()
   serializer_class = AddressSerializer

class RetrieveCustomAddress(APIView):

   def get(self,request,*arg,**kwargs):
      customer =get_object_or_404(Customer,pk=kwargs.get('pk',None))
      if customer is not None:
       addr = get_object_or_404(Address,customer_id=customer)
     
       serializers = AddressSerializer(addr)
         # Generate confirmation token and activation link
       confirmation_token = default_token_generator.make_token(user)
       activate_link_url = reverse('activate')
       activation_link = f'{activate_link_url}?user_id={user.id}&confirmation_token={confirmation_token}'

       return Response(serializers.data)
      else:
       return Response({
          "detail":"there is no related customer with by that id"
       },status=HTTP_404_NOT_FOUND)


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
      oldreiview =ReviewRating.objects.filter(customer = serializer.validated_data['customer'])
      if not oldreiview.exists():


        if pro.avg_rating == 0:
         pro.avg_rating = serializer.validated_data['rating'] 

       
        else:
         pro.avg_rating =  (pro.avg_rating +  serializer.validated_data['rating'] )/2
        pro.save()  
        return serializer.save(product =pro )
      else:
        raise ValidationError({
           'message':'You cannot make a duplicate review only in 1 post'
        })
      
   def create(self, request, *args, **kwargs):
      return super().create(request, *args, **kwargs)

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
  
  

@api_view(['POST'])
def logincustomer(request):
    serializers =  CustomerSerializerLogin(data=request.data)

    if serializers.is_valid():       


        try:
         user = Customer.objects.get(email = serializers.validated_data['email'], is_activated = True)
         hashed_pwd = make_password(serializers.validated_data['password'])

         if check_password(serializers.validated_data['password'],user.password) :

         
          refresh = RefreshToken.for_user( user )
          token = {
       'refresh': str(refresh),
       'access': str(refresh.access_token),
          }
          return Response(token)
         else:
          return Response({
             "message":"wrong user credential"
          },status=HTTP_401_UNAUTHORIZED)
        except Customer.DoesNotExist:
          return Response({
             "data":"there is no user associated with please create an account"
          },status=HTTP_400_BAD_REQUEST)
      

       
    else:
       #validation error
       return Response(serializers.errors,status=HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def socialauth(request):
  serializers = CustomerSerializerV2(data=request.data)
  print(request.data)
  if serializers.is_valid():
   text = serializers.validated_data["username"]
   arr = text.split(" ")
   print(arr[len(  arr )-1])
   thisfirstname = arr[0]
   thislastname = arr[1]
   thisusername = arr[len(  arr )-1]
   serializers.save(username = thisusername,firstname = thisfirstname,
                    lastname = thislastname,telephone = '+41524204242'
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
    