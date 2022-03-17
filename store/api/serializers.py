from rest_framework import serializers

from main.models import Product, Category, Brand



class CategoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class BrandModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


class ProductModelSerializer(serializers.ModelSerializer):
    category = CategoryModelSerializer()
    brand = BrandModelSerializer()

    class Meta:
        model = Product
        fields = '__all__'
