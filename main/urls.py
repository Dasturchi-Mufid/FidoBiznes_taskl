from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi
from .views import UserViewSet, CardViewSet, MerchantCategoryViewSet, MerchantViewSet, TransactionViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# jwt_auth = openapi.SecurityScheme(
#     'Bearer',  # Name of the security scheme
#     openapi.IN_HEADER,  # Location of the token (in HTTP headers)
#     description='JWT Authorization using the Bearer scheme (token must be prefixed with "Bearer ")\nExample: "Authorization: Bearer <Your_Token>"'
# )


schema_view = get_schema_view(
   openapi.Info(
      title="Payment System API",
      default_version='v1',
      description="API documentation for the Payment System",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@paymentsystem.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cards', CardViewSet)
router.register(r'merchant-categories', MerchantCategoryViewSet)
router.register(r'merchants', MerchantViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
