# accounts/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Token
from django.utils import timezone

@receiver(post_migrate)
def clear_expired_tokens(sender, **kwargs):
    Token.objects.filter(expiration__lt=timezone.now()).delete()