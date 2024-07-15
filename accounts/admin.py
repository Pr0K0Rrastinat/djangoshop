from django.contrib import admin
from accounts.models import CustomUser,Token

admin.site.register(CustomUser)
admin.site.register(Token)

