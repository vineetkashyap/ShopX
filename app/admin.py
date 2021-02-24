from django.contrib import admin
from.models import Product,Customer,OrderPlaced,Cart
from django.contrib.auth.models import User
# Register your models here.

@admin.register(Cart)
class  AdminCart(admin.ModelAdmin):
    list_display = ('id','user','product','quantity')
@admin.register(Customer)
class  AdminCustomer(admin.ModelAdmin):
    list_display = ('id','user','name','locality','city','zipcode','state')

@admin.register(Product)
class  AdminProduct(admin.ModelAdmin):
    list_display = ('id','title','selling_price','discount_price','discription','brand','category','product_image')

@admin.register(OrderPlaced)
class  AdminOrder(admin.ModelAdmin):
    list_display = ('id','user','customer','product','quantity','orderplaced_time','status')