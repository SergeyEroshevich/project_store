from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product, Profile
from .cart import Cart

from main.forms import OrderForm

from main.models import Order


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # form = CartAddProductForm(request.POST)
    # if form.is_valid():
    #     cd = form.cleaned_data
    #     cart.add(product=product,
    #              quantity=cd['quantity'],
    #              update_quantity=cd['update'])
    stock =  int(request.POST.get('stock'))
    cart.add(product=product,  quantity=stock)

    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})

@login_required()
def order_create(request):
    Profile.objects.get_or_create(user=request.user)
    cart = Cart(request)
    items = []
    for item in cart:
        if item['quantity'] > item['product'].stock:
            error = f'Количество товара которое вы указали превышает количество допустимого '
            context = {'error': error }
            return render(request, 'cart_detail.html', context)
        product = Product.objects.get(name=item['product'])

        items.append(product)
    form = OrderForm(initial={'adress': request.user.profile.adress, 'total': cart.get_total_price(), 'phone': request.user.profile.phone})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(buyer=request.user, **form.cleaned_data)
            order.save()
            for item in cart:
                product = Product.objects.get(name=item['product'])
                order.products.add(product)
                product.stock = product.stock - item['quantity']
                product.save()
            cart.clear()
    context = {'form': form, 'products':items, 'total': cart.get_total_price()}
    return render(request, 'make_order.html', context)


