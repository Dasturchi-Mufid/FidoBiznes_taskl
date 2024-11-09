from rest_framework import serializers
from .models import User, Card, Merchant, MerchantCategory, Transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'user', 'card_number', 'card_type', 'bank_name', 'balance']

class MerchantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantCategory
        fields = ['id', 'name', 'description']

class MerchantSerializer(serializers.ModelSerializer):
    category = MerchantCategorySerializer()

    class Meta:
        model = Merchant
        fields = ['id', 'name', 'phone_number', 'category']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'merchant', 'amount', 'phone_number', 'transaction_date', 'device_id', 'ip_address']
