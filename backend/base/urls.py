from django.urls import path
from .views import GetRoutes, GetProducts, GetProduct, MyTokenObtainPairView, GetUserProfile, UpdateUserProfile, GetUsers, RegisterUser
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path("users/login/", MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("user/register/", RegisterUser.as_view(), name='register'),
    path("", GetRoutes.as_view(), name="routes"),
    path("products/", GetProducts.as_view(), name="products"),
    path("users/", GetUsers.as_view(), name="users"),
    path("user/profile/", GetUserProfile.as_view(), name="user-profile"),
    path("user/profile/update/", UpdateUserProfile.as_view(), name="user-profile-update"),
    path("product/<str:pk>/", GetProduct.as_view(), name="product"),
]
