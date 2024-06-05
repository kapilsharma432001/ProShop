from rest_framework.response import Response
from rest_framework.views import APIView
from .products import products
from .serializer import ProductSerializer
from .models import Product

# Create your views here.
class GetRoutes(APIView):
    def get(self, request):
        return Response('Hello')
    

class GetProducts(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    

class GetProduct(APIView):
    def get(self, request, pk):
       product = Product.objects.get(_id=pk)
       serializer = ProductSerializer(product, many=False)
       return Response(serializer.data)
    
    




