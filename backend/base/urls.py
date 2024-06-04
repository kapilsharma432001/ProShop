from django.urls import path
from .views import GetRoutes, GetProducts, GetProduct

urlpatterns = [
    path("", GetRoutes.as_view(), name="routes"),
    path("products/", GetProducts.as_view(), name="products"),
    path("product/<str:pk>/", GetProduct.as_view(), name="product"),
]
