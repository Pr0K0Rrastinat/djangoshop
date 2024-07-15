from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import jwt
from django.conf import settings
import datetime

class CustomUser(AbstractUser):
    class Meta:
        app_label = 'accounts'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True
    )
    token_key = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.token_key:
            self.token_key = self.generate_token()
        super().save(*args, **kwargs)

    def generate_token(self):
        payload = {'user_id': self.id, 'exp': timezone.now() + timezone.timedelta(hours=1)}
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
    
    def is_token_expired(self):
        if self.token_key:
            payload = jwt.decode(self.token_key, settings.SECRET_KEY, algorithms=['HS256'])
            expiration = payload.get('exp')
            return timezone.now() > timezone.make_aware(datetime.datetime.fromtimestamp(expiration))
        return True

    @staticmethod
    def clear_expired_tokens():
        expired_tokens = Token.objects.filter(expiration__lt=timezone.now())
        expired_tokens.delete()

class Token(models.Model):
    key = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='token', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    expiration = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expiration:
            self.expiration = timezone.now() + timezone.timedelta(hours=1)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return self.expiration < timezone.now()
