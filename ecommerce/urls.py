from django.contrib import admin
from django.urls import path,include
from . import views

from rest_framework.authtoken.views import obtain_auth_token




urlpatterns = [
   path('product',views.ProductList.as_view(),name='list-product'),
   path('product/<int:pk>',views.ProductRUD.as_view(),name='retrieve-update-delete-product'),
   path('product/create',views.ProductCreate.as_view(),name='list-product'),

    #category
   path('product/category',views.CategoryList.as_view(),name='list-product'),
   path('product/category/create',views.CategoryCreate.as_view(),name='list-product'),
   path('product/category/<int:pk>',views.CategoryRUD.as_view(),name='list-product'),
    #order
    
   path('product/order',views.OrderDetailView.as_view(),name='list-product'),
   path('product/order/<int:pk>',views.OrderDetailRetriandDelete.as_view(),name='list-product'),
   path('product/order/product',views.OrderDetailCreate.as_view(),name='create-list-product'),
   path('product/order-status/<int:pk>',views.OrderStatus,name='order-status'),
  

   
   #review product


   path('product/review',views.ReviewList.as_view(),name='review-product'),
   path('product/review/<int:pk>',views. ReviewRUD.as_view(),name='review-product'),
    # Json Web Token
    # path('product/login', views.CustomTokenObtainPairView.as_view()),
    path('auth/login',views.logincustomer,name="login"),
    path('auth/register',views.register,name="register") ,
    path('auth/google',views.socialauth,name="login-google"),
     # Google Sign in Token
     
    path('auth/reset',views.ResetPW,name="reset-password1"),
    path('auth/reset/verify',views.VerifyCodePW,name="reset-password2"),

    path('activate/', views.activate, name='activate'),

    

    #Address user
    path('address',views.AddressList.as_view(),name="address-list-user"),
    path('address/<int:pk>',views.AddressSingle.as_view(),name="address-single"),
     path('address/customer/<int:pk>',views.RetrieveCustomAddress.as_view(),name="address-single-user"),
      path('address/user/<int:pid>',views.AddressCreate.as_view(),name="address-list-user"),

    #Upload image
     path('image',views.ImageCreate.as_view(),name="img_upload"),
    #  path('image',views.ImageCreate.as_view(),name="img_upload"),
   path('image/<int:pk>',views.ImageRUD.as_view(),name="img_upload")

]