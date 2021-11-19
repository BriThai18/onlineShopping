from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm, ShippingAddressForm
from .utils import userAuthentication, departmentAuthentication

import datetime

# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            Customer.objects.create(user=user, name=user.username, email=user.email)
            return redirect('store')
    context = {'form': form}
    return render(request, 'store/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
    return render(request, 'store/login.html')

def logoutPage(request):
    logout(request)
    return redirect('store')

def store(request):
    context = userAuthentication(request)
    return render(request, 'store/store.html', context)

def computer(request):
    department = 'Computers'
    context = departmentAuthentication(request, department)
    return render(request, 'store/computer.html', context)

def smart(request):
    department = 'Smart Home'
    context = departmentAuthentication(request, department)
    return render(request, 'store/smart.html', context)

def pet(request):
    department = 'Pet Supplies'
    context = departmentAuthentication(request, department)
    return render(request, 'store/pet.html', context)
 
def sport(request):
    department = 'Sports'
    context = departmentAuthentication(request, department)
    return render(request, 'store/sport.html', context)

@login_required(login_url='login')
def cart(request):
    customer = Customer.objects.get(user=request.user)
    order = Order.objects.get(customer=customer.id)
    orderItems = order.orderitem_set.all()
    for item in orderItems:
        if item.quantity <= 0:
            item.delete()
    orderItems = order.orderitem_set.all()
    context = {'order': order, 'orderItems': orderItems}
    return render(request, 'store/cart.html', context)

def addCart(request, id):
    product = Product.objects.get(id=id)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if request.method == 'POST':
        orderItem.quantity += 1
        orderItem.save()
        return redirect('store')
    context = {'product': product}
    return render(request, 'store/addCart.html', context)

def view(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'store/view.html', context)

@login_required(login_url='login')
def addQuantity(request, id):
    item = OrderItem.objects.get(id=id)
    print(item.product.name)
    if request.method == 'POST':
        item.quantity += 1
        item.save()
        return redirect('cart')
    context = {'item': item}
    return render(request, 'store/addQuantity.html', context)

@login_required(login_url='login')
def minusQuantity(request, id):
    item = OrderItem.objects.get(id=id)
    if request.method == 'POST':
        item.quantity -= 1
        item.save()
        return redirect('cart')
    context = {'item': item}
    return render(request, 'store/minusQuantity.html', context)

def checkout(request):
    transactionID = datetime.datetime.now().timestamp
    customer = Customer.objects.get(user=request.user)
    order = Order.objects.get(customer=customer.id)
    orderItems = order.orderitem_set.all()

    if request.method == 'POST':
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            zipcode=request.POST['zipcode'],
            country=request.POST['country']
        )
        Payment.objects.create(
            customer=customer,
            order=order,
            cardNumber=request.POST['cardNumber'],
            expiration=request.POST['expMonth'],
            cvv=request.POST['cvv'],
        )
    order.transaction = transactionID
    order.complete = True
    order.save()
    
    context = {'order': order, 'orderItems': orderItems}
    return render(request, 'store/checkout.html', context)