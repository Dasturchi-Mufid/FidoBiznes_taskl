from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Card, Merchant, MerchantCategory, Transaction
from .serializers import UserSerializer, CardSerializer, MerchantSerializer, MerchantCategorySerializer, TransactionSerializer
from twilio.rest import Client
from rest_framework.permissions import IsAuthenticated


# Helper Functions (same as before)
def send_sms(phone_number, code):
    """
    Send SMS verification code using Twilio.
    """
    client = Client('your_twilio_account_sid', 'your_twilio_auth_token')
    message = client.messages.create(
        body=f"Your verification code is {code}",
        from_='your_twilio_phone_number',
        to=phone_number
    )
    return message.sid


def validate_transaction_data(request):
    
    user = request.user
    merchant_id = request.data.get('merchant_id')
    amount = request.data.get('amount')
    phone_number = request.data.get('phone_number')

    if not merchant_id or not amount or not phone_number:
        return None, None, {'error': 'Merchant ID, amount, and phone number are required.'}

    try:
        merchant = Merchant.objects.get(id=merchant_id)
        card = Card.objects.filter(user=user).first()
        if card.balance < amount:
            return None, None, {'error': 'Insufficient funds.'}
        return merchant, card, None
    except Merchant.DoesNotExist:
        return None, None, {'error': 'Merchant not found.'}


def create_transaction(user, merchant, card, amount, phone_number, device_id, ip_address):
    """
    Create a transaction and deduct balance from the user's card.
    """
    transaction = Transaction.objects.create(
        user=user,
        merchant=merchant,
        amount=amount,
        phone_number=phone_number,
        device_id=device_id,
        ip_address=ip_address
    )
    
    card.balance -= amount
    card.save()

    return transaction



@api_view(['POST'])
def create_user(request):
    """
    Create a new user.
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_users(request):
    """
    List all users.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user(request, pk):
    """
    Get a user by ID.
    """
    try:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# Update User
# @api_view(['PUT'])
# def update_user(request, pk):
#     """
#     Update a user by ID.
#     """
#     try:
#         user = User.objects.get(pk=pk)
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_user(request, pk):
    """
    Delete a user by ID.
    """
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def create_card(request):
    """
    Create a new card.
    """
    if request.method == 'POST':
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_cards(request):
    """
    List all cards.
    """
    cards = Card.objects.all()
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_card(request, pk):
    """
    Get a card by ID.
    """
    try:
        card = Card.objects.get(pk=pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)
    except Card.DoesNotExist:
        return Response({'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_card(request, pk):
    """
    Update a card by ID.
    """
    try:
        card = Card.objects.get(pk=pk)
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Card.DoesNotExist:
        return Response({'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
def delete_card(request, pk):
    """
    Delete a card by ID.
    """
    try:
        card = Card.objects.get(pk=pk)
        card.delete()
        return Response({'message': 'Card deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Card.DoesNotExist:
        return Response({'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_merchant(request):
    """
    Create a new merchant.
    """
    if request.method == 'POST':
        serializer = MerchantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_merchants(request):
    """
    List all merchants.
    """
    merchants = Merchant.objects.all()
    serializer = MerchantSerializer(merchants, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_merchant(request, pk):
    """
    Get a merchant by ID.
    """
    try:
        merchant = Merchant.objects.get(pk=pk)
        serializer = MerchantSerializer(merchant)
        return Response(serializer.data)
    except Merchant.DoesNotExist:
        return Response({'error': 'Merchant not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
def delete_merchant(request, pk):
    """
    Delete a specific merchant by ID.
    """
    try:
        merchant = Merchant.objects.get(pk=pk)
        merchant.delete()
        return Response({'message': 'Merchant deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Merchant.DoesNotExist:
        return Response({'error': 'Merchant not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def create_transaction_view(request):
    """
    Create a new transaction.
    """
    user = request.user
    amount = request.data.get('amount')
    phone_number = request.data.get('phone_number')
    device_id = request.data.get('device_id')
    ip_address = request.META.get('REMOTE_ADDR')


    merchant, card, error_response = validate_transaction_data(request)
    if error_response:
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


    transaction = create_transaction(user, merchant, card, amount, phone_number, device_id, ip_address)

    return Response({'message': 'Transaction successful.', 'transaction_id': transaction.id}, 
                     status=status.HTTP_201_CREATED)



@api_view(['GET'])
def list_transactions(request):
    """
    List all transactions.
    """
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_transaction(request, pk):
    """
    Get a transaction by ID.
    """
    try:
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
def delete_transaction(request, pk):
    """
    Delete a transaction by ID.
    """
    try:
        transaction = Transaction.objects.get(pk=pk)
        transaction.delete()
        return Response({'message': 'Transaction deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def create_merchant_category(request):
    """
    Create a new Merchant Category.
    """
    if request.method == 'POST':
        serializer = MerchantCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def list_merchant_categories(request):
    """
    List all Merchant Categories.
    """
    categories = MerchantCategory.objects.all()
    serializer = MerchantCategorySerializer(categories, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_merchant_category(request, pk):
    """
    Get a Merchant Category by ID.
    """
    try:
        category = MerchantCategory.objects.get(pk=pk)
        serializer = MerchantCategorySerializer(category)
        return Response(serializer.data)
    except MerchantCategory.DoesNotExist:
        return Response({'error': 'Merchant Category not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
def update_merchant_category(request, pk):
    """
    Update a Merchant Category by ID.
    """
    try:
        category = MerchantCategory.objects.get(pk=pk)
        serializer = MerchantCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except MerchantCategory.DoesNotExist:
        return Response({'error': 'Merchant Category not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
def delete_merchant_category(request, pk):
    """
    Delete a Merchant Category by ID.
    """
    try:
        category = MerchantCategory.objects.get(pk=pk)
        category.delete()
        return Response({'message': 'Merchant Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except MerchantCategory.DoesNotExist:
        return Response({'error': 'Merchant Category not found'}, status=status.HTTP_404_NOT_FOUND)