from rest_framework import viewsets
from .models import User, Card, Merchant, MerchantCategory, Transaction
from .serializers import UserSerializer, CardSerializer, MerchantSerializer, MerchantCategorySerializer, TransactionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from twilio.rest import Client
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def verify_phone_number(self, request):
        phone_number = request.data.get('phone_number')
        if phone_number:
            # Send verification code via Twilio
            verification_code = '123456'  # In production, generate a random code
            self.send_sms(phone_number, verification_code)
            return Response({'message': 'Verification code sent.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

    def send_sms(self, phone_number, code):
        client = Client('your_twilio_account_sid', 'your_twilio_auth_token')
        message = client.messages.create(
            body=f"Your verification code is {code}",
            from_='your_twilio_phone_number',
            to=phone_number
        )
        return message.sid


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class MerchantCategoryViewSet(viewsets.ModelViewSet):
    queryset = MerchantCategory.objects.all()
    serializer_class = MerchantCategorySerializer


class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['post'])
    def make_transaction(self, request):
        user = request.user
        merchant_id = request.data.get('merchant_id')
        amount = request.data.get('amount')
        phone_number = request.data.get('phone_number')
        device_id = request.data.get('device_id')
        ip_address = request.META.get('REMOTE_ADDR')

        if not merchant_id or not amount or not phone_number:
            return Response({'error': 'Merchant ID, amount, and phone number are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Find the merchant and check if the user has sufficient balance
        try:
            merchant = Merchant.objects.get(id=merchant_id)
            card = Card.objects.filter(user=user).first()
            if card.balance < amount:
                return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the transaction
            transaction = Transaction.objects.create(
                user=user,
                merchant=merchant,
                amount=amount,
                phone_number=phone_number,
                device_id=device_id,
                ip_address=ip_address
            )
            # Deduct balance from the user's card
            card.balance -= amount
            card.save()

            return Response({'message': 'Transaction successful.', 'transaction_id': transaction.id}, 
                            status=status.HTTP_201_CREATED)
        except Merchant.DoesNotExist:
            return Response({'error': 'Merchant not found.'}, status=status.HTTP_400_BAD_REQUEST)

