from typing import Any, Dict, Optional, Type, TypeVar

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .products import products
from .serializer import ProductSerializer, UserSerializer, UserSerializerWithToken, OrderSerializer
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status


# For another API
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Question
from .serializer import CategorySerializer, QuestionSerializer
from django.db.models import Sum


# For another project APIs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category, Question
from .serializer import CategorySerializer, QuestionSerializer
from django.db.models import Sum


# For updating question responses
class QuestionUpdateResponseView(APIView):
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        response_type = request.data.get('response_type')

        if response_type == 'positive':
            question.positive_answers += 1
        elif response_type == 'negative':
            question.negative_answers += 1
        else:
            question.other_answers += 1

        question.save()
        return Response({'status': 'response updated'}, status=status.HTTP_200_OK)



# Get category count
class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        data = []

        for category in categories:
            positive_count = Question.objects.filter(category=category).aggregate(Sum('positive_answers'))['positive_answers__sum'] or 0
            negative_count = Question.objects.filter(category=category).aggregate(Sum('negative_answers'))['negative_answers__sum'] or 0
            other_count = Question.objects.filter(category=category).aggregate(Sum('other_answers'))['other_answers__sum'] or 0

            data.append({
                'category': category.name,
                'positive': positive_count,
                'negative': negative_count,
                'other': other_count
            })

        return Response(data, status=status.HTTP_200_OK)

###########################


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
    
@permission_classes([IsAuthenticated])
class UpdateUserProfile(APIView):
    def put(self, request):
        user = request.user
        serializer = UserSerializerWithToken(user, many=False)
        data = request.data

        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']

        if data['password'] !='':
            user.password = make_password(data['password'])

        user.save()  

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

    

class GetProduct(APIView):
    def get(self, request, pk):
       product = Product.objects.get(_id=pk)
       serializer = ProductSerializer(product, many=False)
       return Response(serializer.data)
    

class AddOrderItem(APIView):
    def post(self, request):
        user = request.user
        data = request.data

        orderItems = data["orderItems"]

        if orderItems and len(orderItems) == 0:
            return Response({"detail": "No order items"}, status=status.HTTP_400_BAD_REQUEST)    

        # (1) Create Order

        order = Order.objects.create(
            user = user,
            paymentMethod = data["paymentMethod"],
            taxPrice = data["taxPrice"],
            shippingPrice = data["shippingPrice"],
            totalPrice = data["totalPrice"],
        )

        # (2) Create shipping address
        shippingAddress = ShippingAddress.objects.create(
            order = order,
            address = data["shippingAddress"]["address"],
            city = data["shippingAddress"]["city"],
            postalCode = data["shippingAddress"]["postalCode"],
            country = data["shippingAddress"]["country"],
            shippingPrice = data["shippingPrice"]
        )

        # (3) Create order item and set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id = i["product"])

            orderItem = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                qty = i['qty'],
                price = i['price'],
                image = product.image.url
            )

        # (4) Update stock
        product.countInStock -= orderItem.qty
        product.save()

        serializer = OrderSerializer(order, many=False)
        return Response({serializer.data}, status=status.HTTP_202_ACCEPTED)

    
    




