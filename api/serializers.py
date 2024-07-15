from rest_framework import serializers
from shop.models import Order  # Путь к модели Order

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'amount', 'shop_id']
