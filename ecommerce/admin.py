from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
     list_display = ('id','productname','price','stockqty','category','owner',)

class CustomerAdmin(admin.ModelAdmin):
     
     list_display = ('id','username','email','telephone',)
# class OrderDetailAdmin(admin.ModelAdmin):
#      list_display = ('id','created_date','product','qty','amount','method','status')

class Favoriteadmin(admin.ModelAdmin):
     list_display = ('id','user',)
admin.site.register(Favorite,Favoriteadmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
# admin.site.register(Order)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(OrderDetail)
admin.site.register(ReviewRating)
admin.site.register(Address)
admin.site.register(Sizes)
admin.site.register(Images)
admin.site.register(Attributes)
admin.site.register(Colors)
admin.site.register(SuperDeal)
admin.site.register(OrderProduct)
admin.site.register(PasswordResetCodes)






