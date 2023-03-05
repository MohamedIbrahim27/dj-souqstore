from django.shortcuts import render ,redirect
from django.contrib import messages
from product.models import Product
from orders.models import Order
from django.contrib.auth.models import User
from orders.models import OrderDetails
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseForbidden
from accounts.models import Profile
from.models import Checkout

@login_required(login_url='/accounts/signin')
def add_to_cart(request):
    if request.user.is_authenticated:
        if 'product' in request.GET and  'product_price' in request.GET and  'qty' in request.GET:
            product= request.GET['product']
            qty= request.GET['qty']
            order= Order.objects.all().filter(user=request.user,is_finished=False)
            productname=Product.objects.get(slug=product)
            if order:
                old_order=Order.objects.get(user=request.user,is_finished=False)
                if OrderDetails.objects.all().filter(order=old_order,product=productname).exists():
                    order_detials=OrderDetails.objects.get(order=old_order,product=productname)
                    order_detials.quantity += int(qty)
                    order_detials.save()
                else:
                    order_detials=OrderDetails.objects.create(
                        product=productname,
                        order=old_order,
                        cost=productname.PRDCost,
                        quantity=qty)
            else:
                new_order=Order()
                new_order.user=request.user
                new_order.order_date=timezone.now()
                new_order.is_finished=False
                new_order.save()
                order_detials=OrderDetails.objects.create(
                    product=productname,
                    order=new_order,
                    cost=productname.PRDCost,
                    quantity=qty)
            messages.success(request,'Product added successfully To Cart')
            return redirect ('/' + request.GET['product'])
        else:
            messages.error(request,'Error To Add in Cart')
            return redirect ('/' + request.GET['product'])
    else:
    
        messages.error(request,'You Must Be Login')
        return redirect ('/' + request.GET['product'])

@login_required(login_url='/accounts/signin')
def cart(request):
    context=None
    if Order.objects.all().filter(user=request.user,is_finished=False):
        order=Order.objects.get(user=request.user,is_finished=False)
        orderdetials=OrderDetails.objects.all().filter(order=order)
        total=0
        for sub in orderdetials:
            total += sub.cost * sub.quantity
        context={
            'order':order,
            'orderdetials':orderdetials,
            'total':total,
        }
    return render(request,'order/cart.html', context)

@login_required(login_url='/accounts/signin')
def remove_from_Cart(request,orderdetials_id):
    orderdetials=OrderDetails.objects.get(id=orderdetials_id)
    if request.user.id == orderdetials.order.user.id:
        orderdetials.delete()
        return redirect('/orders/cart')
    else:
        return HttpResponseForbidden("You don't have permission to edit this cart .")

@login_required(login_url='/accounts/signin')
def clear_Cart(request):
    order=Order.objects.get(user=request.user)
    OrderDetails.objects.all().filter(order=order).delete()
    return redirect('/orders/cart')

def add_qty(request,orderdetials_id):
    if orderdetials_id:
        orderdetials=OrderDetails.objects.get(id=orderdetials_id)
        orderdetials.quantity +=1
        orderdetials.save()
    return redirect('/orders/cart')
def sub_qty(request,orderdetials_id):
    if orderdetials_id:
        orderdetials=OrderDetails.objects.get(id=orderdetials_id)
        if orderdetials.quantity > 1:
            orderdetials.quantity -=1
            orderdetials.save()
    return redirect('/orders/cart')

def ckeck_out(request):
    context=None
    user_profile=Profile.objects.get(user=request.user)
    cardholder=None
    cardnumber=None
    expire=None
    security=None
    if request.method=='POST' and 'cardnumber' in request.POST and 'cardholder' in request.POST and 'security' in request.POST and 'expire' in request.POST:

        cardholder=request.POST['cardholder']
        cardnumber=request.POST['cardnumber']
        expire=request.POST['expire']
        security=request.POST['security']
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order=Order.objects.get(user=request.user,is_finished=False)
            checkout=Checkout(order=order,
                            country=user_profile.country.name,
                            adress=user_profile.adress,
                            phone=user_profile.phone,
                            cardholder=cardholder,
                            cardnumber=cardnumber,
                            expire=expire,
                            security=security)
            checkout.save()
            order.is_finished=True
            order.save()
            return redirect('/')
    else:
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order=Order.objects.get(user=request.user,is_finished=False)
            orderdetials=OrderDetails.objects.all().filter(order=order)
            total=0
            for sub in orderdetials:
                total += sub.cost * sub.quantity
            context={
                'order':order,
                'orderdetials':orderdetials,
                'total':total,
            }
    return render(request,'order/checkout.html',context)