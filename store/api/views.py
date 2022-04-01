from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.response import Response
from main.models import Product, Brand
from rest_framework.views import APIView

from .serializers import ProductModelSerializer, BrandModelSerializer


@api_view(['GET'])
def products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductModelSerializer(products, many=True)
        return Response(serializer.data)


class BrandApi(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandModelSerializer(brands, many=True)
        return Response (serializer.data)

    def post(self, request):
        serializer = BrandModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



