from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
    )

    def __str__(self):
        return self.username


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20)
    card_type = models.CharField(choices=[('HUMO', 'HUMO'), ('UzCard', 'UzCard')], max_length=10)
    bank_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.card_type} - {self.card_number}'


class MerchantCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Merchant(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    category = models.ForeignKey(MerchantCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    transaction_date = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f'Transaction: {self.id} - {self.user.username}'
