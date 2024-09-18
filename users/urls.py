from django.urls import path
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import (
    PaymentListAPIView,
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    PaymentCreateAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("list/", UserListAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/detail/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("users/<int:pk>/destroy/", UserDestroyAPIView.as_view(), name="user_destroy"),
    path("payment/", PaymentCreateAPIView.as_view(), name="payment-create"),
]
