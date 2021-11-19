from .models import *

def userAuthentication(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.get(customer=customer.id)
        return {'products': products, 'order': order}
    else:
        return {'products': products}

def departmentAuthentication(request, department):
    products = Product.objects.filter(department=department)
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.get(customer=customer.id)
        return {'products': products, 'order': order}
    else:
        return {'products': products}
