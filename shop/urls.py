from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_list, name='shop_list'),
    path('shops/', views.shop_list, name='shop_list'),
    path('shops/<int:pk>/', views.shop_detail, name='shop_detail'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
]