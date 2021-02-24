from django.shortcuts import render,HttpResponseRedirect,redirect
from django.views import View
from.models import Product,Customer,OrderPlaced,Cart
from .forms import SignUpForm,LoginForm,CustomerProfileForm
from django.contrib.auth import login,logout ,authenticate
from django.contrib import  messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic.base import RedirectView
class Home(View):
    def get(self,request):
        product = Product.objects.filter(category='bw')
        mobile = Product.objects.filter(category='m')
        topwear  = Product.objects.filter(category='tw')
        return render(request,'app/home.html',{'product':product,'mobile':mobile,'top':topwear})
@login_required
def product_detail(request,id):
      product = Product.objects.get(pk=id)
      item_already_in_cart =False
      if request.user.is_authenticated:
           item_already_in_cart = Cart.objects.filter(Q(user=request.user)&Q(product=product.id)).exists()

      
      return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

    
def add_to_cart(request):
    user =request.user
    cart =Cart.objects.filter(user=user)
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return render(request,'app/addtocart.html',{'carts':cart})

def show_cart(request):
    if request.user.is_authenticated:
        user =request.user
        cart =Cart.objects.filter(user=user)
        print('======vineet===============>>>>>>>>>>>>',cart)
        cart_product = [p for  p in Cart.objects.all().filter(user=user)]
        amount= 0.0
        shipping_amount=70
        if cart_product:
            for p in cart_product:
                tempamount = (p.product.discount_price*p.quantity)
                amount +=tempamount
                total_amount = amount+shipping_amount
            amount=int(amount)
            return render(request, 'app/addtocart.html',{'total_amount':total_amount,'amount':amount,'carts':cart})  
        else:
            return render(request,'app/emptycart.html')

def pluscart(request):
     if request.method == 'GET':
         prod_id =request.GET['prod_id']
         c=Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
         c.quantity+=1
         c.save()
         cart_product = [p for  p in Cart.objects.all().filter(user=request.user)]
         amount= 0.0
         shipping_amount=70
         if cart_product:
            for p in cart_product:
                tempamount = (p.product.discount_price*p.quantity)
                amount +=tempamount
               
            if amount== 0:
                  total_amount =amount
            else:
                 total_amount = amount+shipping_amount

            amount=int(amount)
         data={
             'quantity': c.quantity,
             'amount':amount,
             'total_amount':total_amount

          }
         return JsonResponse(data)

def minuscart(request):
     if request.method == 'GET':
         prod_id =request.GET['prod_id']
         c=Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
         c.quantity-=1
         c.save()
         cart_product = [p for  p in Cart.objects.all().filter(user=request.user)]
         amount= 0.0
         shipping_amount=70
         if cart_product:
            for p in cart_product:
                tempamount = (p.product.discount_price*p.quantity)
                amount +=tempamount
            if amount== 0:
                  total_amount =amount
            else:
                 total_amount = amount+shipping_amount
                
            amount=int(amount)
         data={
             'quantity': c.quantity,
             'amount':amount,
             'total_amount':   total_amount 

          }
         return JsonResponse(data)

def removecart(request):
     if request.method == 'GET':
         prod_id =request.GET['prod_id']
         c=Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
         c.delete()
         cart_product = [p for  p in Cart.objects.all().filter(user=request.user)]
         amount= 0.0
         total_amount=0
         shipping_amount=70
         if cart_product:
            for p in cart_product:
                tempamount = (p.product.discount_price*p.quantity)
                amount +=tempamount
            if amount== 0:
                  total_amount =amount
            else:
                 total_amount = amount+shipping_amount
                
            amount=int(amount)
         data={
             'amount':amount,
             'total_amount':   total_amount 

          }       
         return JsonResponse(data)
        

def buy_now(request):
  return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

def address(request):
 address = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'address':address})

def orders(request):
    order_placed =  OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'orders':order_placed})

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data == None:
         mobile = Product.objects.filter(category='m')
    elif data == 'redmi' or data == 'samsung':
         mobile = Product.objects.filter(category='m').filter(brand=data)
    elif data =='below' :
        mobile = Product.objects.filter(category='m').filter(discount_price__lt=10000)
    elif data =='above' :
        mobile = Product.objects.filter(category='m').filter(discount_price__gt=10000)
    return render(request, 'app/mobile.html',{'mobile':mobile})

         

class CustomerRegistrationForm(View):
    def get(self,request):
         form = SignUpForm()
         return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        fm = SignUpForm(request.POST)
        if fm.is_valid():
           fm.save()  
           messages.success(request,'Registraion Successfully')
        form = SignUpForm()
        return render(request, 'app/customerregistration.html',{'form':form})
@method_decorator(login_required,name='dispatch' )
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr =request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            reg = Customer(user=usr,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
            reg.save()
            messages.success(request,'Address Added Successfully')
            form = CustomerProfileForm()
            return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
def checkout(request):
    user= request.user
    add = Customer.objects.filter(user=user)
    cart_items =Cart.objects.filter(user=user)
    amount = 0.0
    total_amount=0
    shipping_amount = 70
    cart_product = [p for p in Cart.objects.all() if p.user==user]
    if cart_product:
          if cart_product:
            for p in cart_product:
                tempamount = (p.product.discount_price*p.quantity)
                amount +=tempamount
            total_amount = amount+shipping_amount   
         

    return render(request, 'app/checkout.html',{'add':add,'total_amount':total_amount,'cart_items':cart_items})        


def payment_done(request):
    user=request.user
    custid =request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart =Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()    
    #email sending function
    def emailsend():
        template = render_to_string('app/email.html',{'name':request.user.username})
        email = EmailMessage(
            'Thanks for purchasing the stuff from us',
            template,
            settings.EMAIL_HOST_USER,
            [request.user.email],
        )
        email.fail_silently=False
        email.send()
        
        return redirect("orders")    
    emailsend() 
    return redirect('orders')
      
def searchbar(request):
    search_entry = request.GET.get('search_item')
    search_data = Product.objects.filter(title__icontains=search_entry)
    print('==========search item==================>',search_entry)
    return render(request,'app/searchbar.html',{'search_data':search_data})


