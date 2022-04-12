

from django.urls import path

from .views import products, BrandApi

app_name = 'api'

urlpatterns = [
    path('products/', products, name='products'),
    path('brands/', BrandApi.as_view(), name='brands'),

]