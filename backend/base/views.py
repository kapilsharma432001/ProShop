from rest_framework.response import Response
from rest_framework.views import APIView
from .products import products

# Create your views here.
class GetRoutes(APIView):
    def get(self, request):
        return Response('Hello')
    

class GetProducts(APIView):
    def get(self, request):
        return Response(products)
    

class GetProduct(APIView):
    def get(self, request, pk):
        product = None
        for i in products:
            if i["_id"] == pk:
                product = i
                break
        return Response(product)
    
    




