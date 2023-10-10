from django.contrib import admin
from django.urls import path,include
from . import views

from rest_framework.authtoken.views import obtain_auth_token




urlpatterns = [
   path('product',views.ProductList.as_view(),name='list-product'),
   path('product/sort',views.ProductListSort.as_view(),name='list-product'),
   path('product/discount/',views.ProductDiscount.as_view(),name='list-product'),
   path('product/<int:pk>',views.ProductRUD.as_view(),name='retrieve-update-delete-product'),
   path('product/create',views.ProductCreate.as_view(),name='list-product'),

    #category
   path('category',views.CategoryList.as_view(),name='list-product'),
   path('category/create',views.CategoryCreate.as_view(),name='list-product'),
   path('category/<int:pk>',views.CategoryRUD.as_view(),name='list-product'),
    #order
    
   path('order',views.OrderDetailView.as_view(),name='list-product'),
      path('order/user/<int:pk>',views.OrderUserView.as_view(),name='list-product-user'),
   path('order/<int:pk>',views.OrderDetailRetriandDelete.as_view(),name='list-product'),
   path('order/product/<int:pk>',views.OrderDetailCreate.as_view(),name='create-list-product'),
   path('order-status/<int:pk>',views.OrderStatus,name='order-status'),
  

   
   #review product


   path('review/product/',views.ReviewList.as_view(),name='review-product'),
   path('review/<int:pk>',views. ReviewRUD.as_view(),name='review-product'),
   path('review/product/<int:pk>',views. ReviewProduct.as_view(),name='review-product-v2'),
    # Json Web Token
    # path('product/login', views.CustomTokenObtainPairView.as_view()),
    path('auth/login',views.logincustomer,name="login"),
    
    path('auth/register',views.register,name="register") ,
    path('auth/google',views.socialauth,name="login-google"),
   path('auth/update/<int:pk>',views.updateuserprofile,name="login-google-profile"),
     # Google Sign in Token
     
    path('auth/reset',views.ResetPW,name="reset-password1"),
    path('auth/reset/verify',views.VerifyCodePW,name="reset-password2"),
    path('auth/user/<int:pk>',views.finduser,name="user"),
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