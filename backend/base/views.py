from typing import Any, Dict, Optional, Type, TypeVar

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .products import products
from .serializer import ProductSerializer, UserSerializer, UserSerializerWithToken
from .models import Product
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
       
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k] = v
        
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Create your views here.
class GetRoutes(APIView):
    def get(self, request):
        return Response('Hello')

@permission_classes([IsAuthenticated])
class GetUserProfile(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

class GetProducts(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

@permission_classes([IsAdminUser])  
class GetUsers(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class RegisterUser(APIView):
    def post(self, request):
        try:
            data = request.data

            user = User.objects.create(
                first_name = data['name'],
                username = data['email'],
                email = data['email'],
                password = make_password(data['password'])
            )

            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except Exception as e:
            message = {"message":"User with this email already exists"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    
@permission_classes([IsAdminUser, IsAuthenticated])
class GetProduct(APIView):
    def get(self, request, pk):
       product = Product.objects.get(_id=pk)
       serializer = ProductSerializer(product, many=False)
       return Response(serializer.data)
    


    
    




