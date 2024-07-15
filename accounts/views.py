from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.urls import reverse
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.urls import reverse
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
import jwt
from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote
from django.conf import settings
import jwt

def login_view(request):
    if request.user.is_authenticated:
        print("===Hola===")
        return redirect(reverse('shop_list'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token = user.generate_token()  # Generate a new token on login
            response = redirect(next_url if next_url else reverse('shop_list'))
            response['Authorization'] = f'Bearer {token}'  # Set token in response header
            return response
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('shop_list')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def logout_view(request):
    Token.objects.filter(user=request.user).delete()
    logout(request)
    return redirect('login')
