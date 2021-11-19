from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('computer/', views.computer, name='computer'),
    path('sport/', views.sport, name='sport'),
    path('pet/', views.pet, name='pet'),
    path('smart/', views.smart, name='smart'),
    path('cart/', views.cart, name='cart'),
    path('register/', views.register, name='register'),
    path('addCart/<int:id>', views.addCart, name='addCart'),
    path('view/<int:id>', views.view, name='view'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('addQuantity/<int:id>', views.addQuantity, name='addQuantity'),
    path('minusQuantity/<int:id>', views.minusQuantity, name='minusQuantity'),
    path('checkout/', views.checkout, name='checkout')
]