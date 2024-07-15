from django.urls import path
from .views import UpdateOrderStatusAPI

urlpatterns = [
    path('orders/<int:pk>/update_status/', UpdateOrderStatusAPI.as_view(), name='update_order_status'),
]
