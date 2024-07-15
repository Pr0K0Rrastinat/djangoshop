from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.urls import reverse
from urllib.parse import urlencode
import requests
from shop.models import Order,Shop
from django.contrib.auth.decorators import login_required
from api.serializers import OrderDetailSerializer  

def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'shop_list.html', {'shops': shops})

def shop_detail(request, pk):
    shop = Shop.objects.get(pk=pk)
    orders = Order.objects.filter(shop=shop)
    return render(request, 'shop_detail.html', {'shop': shop, 'orders': orders})

@login_required(login_url='login')
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return HttpResponseNotFound("Order not found")
    if order.shop.open == False:  # Проверяем, закрыт ли магазин
        return HttpResponseForbidden("Нельзя внести изменения. Магазин закрыт")
    
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order.status = new_status
        order.updated_by = request.user  # Записываем пользователя, который изменил статус
        order.save()

        if order.status == "завершен":
            api_url = f'http://127.0.0.1:8000/api/orders/{pk}/update_status/'
            headers = {'Authorization': f'Token {request.user.token_key}'}
            response = requests.post(api_url, data={'new_status': new_status}, headers=headers)
            if response.status_code == 403:
                return redirect(f"{reverse('login')}?next={urlencode({'next': request.get_full_path()})}")
            elif response.status_code == 200:
                print("====Данные успешно отправлены===")
            else:
                print(f'Error updating order status: {response.text}')

    return render(request, 'order_detail.html', {'order': order})