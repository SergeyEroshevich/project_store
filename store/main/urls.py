from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import main, add_product, product_detail, make_order, contacts, profile_logout, registration, to_profile, \
    profile, change_profile, my_orders, order_details, rating_product, order_details_for_buyer, all_orders, discounts, \
    shipping_payment, discount_managment

app_name = 'main'
urlpatterns = [
    path('', main, name='main'),
    path('add_product/', add_product, name='add_product'),
    path('make_order/<product>', make_order, name='make_order'),
    path('product_detail/<product_id>/<product_slug>', product_detail, name='product_detail'),
    path('contacts/', contacts, name='contacts'),
    path('my_orders/', my_orders, name='my_orders'),
    path('all_orders/<order>/<int:page>/', all_orders, name='all_orders'),
    path('order_details/<order_id>/', order_details, name='order_details'),
    path('order_details_for_buyer/<order_id>/', order_details_for_buyer, name='order_details_for_buyer'),
    path('rating_product/<order_id>/<product_id>/', rating_product, name='rating_product'),
    path('registration/', registration, name='registration'),
    path('accounts/login/', to_profile, name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', change_profile, name='profile_change'),
    path('accounts/logout/', profile_logout, name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view( template_name='password_change_form.html', success_url = reverse_lazy ('main:password_change_done')), name='password_change'),
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view( template_name='password_changed.html'), name='password_change_done'),
    path('shipping&payment/',  shipping_payment, name='shipping_payment'),
    path('discounts/', discounts, name='discounts'),
    path('discount_managment/', discount_managment, name='discount_managment'),
    path('<category_slug>/', main, name='main_category'),

]