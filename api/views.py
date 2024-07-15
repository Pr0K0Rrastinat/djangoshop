from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import Order 
from api.serializers import OrderDetailSerializer  

class UpdateOrderStatusAPI(APIView):

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)
        
        
        updated_order_data = {
            'id': order.id,
            'amount': order.amount,
            'shop_id': order.shop_id,
            'изменен': order.updated_by.username  
            }
        print(f"{updated_order_data}")
        serializer = OrderDetailSerializer(data=updated_order_data)
        if serializer.is_valid():
            return Response(serializer.data)
        
        return Response({'message': 'No changes made to the order status'})
