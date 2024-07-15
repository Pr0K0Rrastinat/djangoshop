from django.db import models
from django.conf import settings

class Shop(models.Model):
    name = models.CharField(max_length=255)
    open = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('готовится', 'Готовится'),
        ('доставка', 'Доставка'),
        ('завершен', 'Завершен'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='готовится')
    amount = models.IntegerField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk and 'updated_by' not in kwargs.get('update_fields', []):
            kwargs['update_fields'] = kwargs.get('update_fields', []) + ['updated_by']
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.pk} - {self.shop.name} - {self.status}"
