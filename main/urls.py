from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views



urlpatterns = [
    # User CRUD
    path('users/', views.list_users, name='list_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:pk>/', views.retrieve_user, name='retrieve_user'),
    path('users/<int:pk>/update/', views.update_user, name='update_user'),
    path('users/<int:pk>/delete/', views.delete_user, name='delete_user'),

    # Card CRUD
    path('cards/', views.list_cards, name='list_cards'),
    path('cards/create/', views.create_card, name='create_card'),
    path('cards/<int:pk>/', views.retrieve_card, name='retrieve_card'),
    path('cards/<int:pk>/update/', views.update_card, name='update_card'),
    path('cards/<int:pk>/delete/', views.delete_card, name='delete_card'),

    # Merchant CRUD
    path('merchants/', views.list_merchants, name='list_merchants'),
    path('merchants/create/', views.create_merchant, name='create_merchant'),
    path('merchants/<int:pk>/', views.retrieve_merchant, name='retrieve_merchant'),
    path('merchants/<int:pk>/update/', views.update_merchant, name='update_merchant'),
    path('merchants/<int:pk>/delete/', views.delete_merchant, name='delete_merchant'),

     # Merchant Category CRUD
    path('merchant-categories/', views.list_merchant_categories, name='list_merchant_categories'),
    path('merchant-categories/create/', views.create_merchant_category, name='create_merchant_category'),
    path('merchant-categories/<int:pk>/', views.retrieve_merchant_category, name='retrieve_merchant_category'),
    path('merchant-categories/<int:pk>/update/', views.update_merchant_category, name='update_merchant_category'),
    path('merchant-categories/<int:pk>/delete/', views.delete_merchant_category, name='delete_merchant_category'),

    # Transaction CRUD
    path('transactions/', views.list_transactions, name='list_transactions'),
    path('transactions/create/', views.create_transaction_view, name='create_transaction'),
    path('transactions/<int:pk>/', views.retrieve_transaction, name='retrieve_transaction'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),

    # JWT Authentication
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
