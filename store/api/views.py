from django.shortcuts import render
from rest_framework.decorators import api_view

from rest_framework.response import Response
from main.models import Product
from .serializers import ProductModelSerializer



@api_view(['GET'])
def products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductModelSerializer(products, many=True)
        return Response(serializer.data)



