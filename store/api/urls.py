

from django.urls import path

from .views import products

app_name = 'api'

urlpatterns = [
    path('', products),

]