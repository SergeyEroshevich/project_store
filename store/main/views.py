from decimal import Decimal

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Count, F, ExpressionWrapper, DecimalField, IntegerField
from django.db.models.functions import Round
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from .forms import ProductForm, LoginForm, RegistrationForm, ChangeUserlnfoForm, OrderForm, SortForm, StatusForm, \
    RatingForm, SearchForm, DiscountForm, DiscountDeleteForm, AdressProfileForm, PhoneProfileForm
from .models import Category, Product, Image, Profile, Order, Rating



def main(request, category_slug = None):
    form = SortForm()
    form_search = SearchForm()
    category = None
    categories = Category.objects.all()
    products = Product.objects.annotate(value_sale=ExpressionWrapper(100 - F('sale') * 100, IntegerField()),
                                        res_sale=Round(ExpressionWrapper(F('price')*F('sale'), DecimalField())), res2=Count('order')).filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if request.method == 'POST':
        if request.POST.get('discount') == 'on':
            products = products.filter(discount=True)
        if request.POST.get('brand'):
            brands = request.POST.getlist('brand')
            products = products.filter(brand__in=[i for i in brands])
        if request.POST.get('price_from'):
            products = products.filter(res_sale__gte=request.POST.get('price_from'))
        if request.POST.get('price_to'):
            products = products.filter(res_sale__lte=request.POST.get('price_to'))

        if request.POST.get('sort'):
            atrr = int(request.POST.get('sort'))
            method_sort = {1: '-price', 2: 'price', 3: '-res2', 4: '-rating', 5: 'created'}

            def sort(method, product):
                products = product.order_by(method)
                return products
            products = sort(method_sort.get(atrr), products)

            # sort = int(request.POST.get('sort'))
            # if sort == 1:
            #     products = products.order_by('-price')
            # if sort == 2:
            #     products = products.order_by('price')
            # if sort == 3:
            #     products = products.order_by('-res2')
            # if sort == 4:
            #     products = products.order_by('-rating')
            # if sort == 5:
            #     products = products.order_by('created')
    context = {'category': category, 'products': products, 'categories': categories, 'form': form, 'form_search': form_search}
    return render(request, 'main.html', context)


def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
        if request.FILES.get('photo_1'):
            Image.objects.create(img=request.FILES['photo_1'], product=product)
        if request.FILES.get('photo_2'):
            Image.objects.create(img=request.FILES['photo_2'], product=product)
        if request.FILES.get('photo_3'):
            Image.objects.create(img=request.FILES['photo_3'], product=product)
        if request.FILES.get('photo_4'):
            Image.objects.create(img=request.FILES['photo_4'], product=product)
    context = {'form': form}
    return render(request, 'add_product.html', context)

@login_required()
def make_order(request, product):
    product = Product.objects.get(name=product)
    Profile.objects.get_or_create(user=request.user)
    total = round(product.price*Decimal(product.sale))
    form = OrderForm(initial={'adress':request.user.profile.adress, 'total':total, 'phone': request.user.profile.phone})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(buyer=request.user, **form.cleaned_data)
            if total < 50 and order.delivery == '????????????':
                order.total = int(order.total) + 7
            elif total < 50 and order.delivery == '??????????':
                order.total = int(order.total) + 7
            order.save()
            order.products.add(product)
        product.stock = product.stock - 1
        product.save()
        return redirect('/my_orders/')
    items = []
    items.append(product)
    context = {'form': form, 'products':items, 'total': total}
    return render(request, 'make_order.html', context)


@receiver(post_save, sender=Order)
def mail_make_order(sender, **kwargs):
    subject = '???????????????????? ???????????? ?? ????????????????'
    html_message = render_to_string('message_order.html', {'order': kwargs.get('instance')})
    plain_message = strip_tags(html_message)
    from_email = 'eroshik.test@gmail.com'
    instance = kwargs.get('instance')
    to_mail = instance.buyer.email
    send_mail(subject, plain_message, from_email, [to_mail], html_message=html_message)


def product_detail(request, product_id, product_slug):
    product = get_object_or_404(Product, id=product_id, slug=product_slug, available=True)
    # cart_product_form = CartAddProductForm()
    img = Image.objects.filter(product_id=product_id)
    context = {'product':product, 'img':img}
    return render(request, 'product_detail.html', context)

def contacts(request):
    return render(request, 'contacts.html')


def to_profile(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
    context = {'form': form}
    return render(request, 'login.html', context)

@login_required()
def profile(request):
    form_adress = AdressProfileForm()
    form_phone = PhoneProfileForm()

    user = request.user
    profile, status = Profile.objects.get_or_create(user=user)
    if request.method == 'POST':

        if request.POST.get('adress'):
            form_adress = AdressProfileForm(request.POST)
            if form_adress.is_valid():
                adress = form_adress.cleaned_data.get('adress')
                profile.adress = adress
                profile.save()

        if request.POST.get('phone'):
            form_phone = PhoneProfileForm(request.POST)
            if form_phone.is_valid():
                phone = form_phone.cleaned_data.get('phone')
                profile.phone = phone
                profile.save()

    context = {'user': user, 'form_adress': form_adress, 'form_phone': form_phone}
    return render(request, 'profile.html', context)


def profile_logout(request):
    logout(request)
    return redirect('/')

def registration(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.pop('phone')
            adress = form.cleaned_data.pop('adress')
            user = User(**form.cleaned_data)
            user.set_password(request.POST['password'])
            user.save()
            profile = Profile(adress=adress, phone=phone, user=user)
            profile.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'registration.html', context)



# @receiver(post_init, sender=User)
def mail_registration(sender, **kwargs):
    subject = '?????????????????????? ???? ?????????? ????????????????-????????????????'
    html_message = render_to_string('message_registration.html', {'user': kwargs.get('instance')})
    plain_message = strip_tags(html_message)
    from_email = 'eroshik.test@gmail.com'
    instance = kwargs.get('instance')
    to_mail = instance.email
    send_mail(subject, plain_message, from_email, [to_mail], html_message=html_message)


@login_required()
def change_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    form = ChangeUserlnfoForm(initial={'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email,
                                       'adress':profile.adress, 'phone':profile.phone})
    if request.method == 'POST':
        form = ChangeUserlnfoForm(request.POST)
        if form.is_valid():
            adress = form.cleaned_data.pop('adress')
            phone = form.cleaned_data.pop('phone')
            profile.adress = adress
            profile.phone = phone
            profile.save()
            user.first_name = form.cleaned_data.pop('first_name')
            user.last_name = form.cleaned_data.pop('last_name')
            user.email = form.cleaned_data.pop('email')
            user.save()
    context = {'form': form}
    return render(request, 'change_user_info.html', context)

def  my_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-data_order')
    context = {'orders': orders}
    return render(request, 'my_orders.html', context)

def all_orders(request, order, page=1):
    all_orders = Order.objects.all().order_by(order).reverse()
    if order == 'data_order':
        all_orders = Order.objects.all().order_by(order)
    if request.method == 'POST':
        n = int(request.POST.get('status'))
        if n == 1:
            all_orders = Order.objects.filter(status='?????????????? ?? ??????????????????')
        elif n == 2:
            all_orders = Order.objects.filter(status='?????????????????? ????????????????????')
        elif n == 3:
            all_orders = Order.objects.filter(status='???????????????? ?? ??????????????????')
        elif n == 4:
            all_orders = Order.objects.filter(status='??????????????')
        elif n == 5:
            all_orders = Order.objects.filter(status='???????????????? ?????????????????????? ????????????')
        elif n == 6:
            all_orders = Order.objects.filter(status='?????????????????? ???????????????????? ?? ???????????????? ????????????')
    n = all_orders.count()
    output = 8 # ???????????????????? ?????????????????? ?????????????? ???? ?????????? ????????????????
    res = n//output + 1
    if n % output != 0:
        res = res + 1
        order_for_page = range(1, res)
    else:
        order_for_page = range(1, res)
    i=1
    while i < res:
        if page==1:
            all_orders = all_orders[:output]
        elif page == 1 + i:
            x = 1 + i
            all_orders = all_orders[output*i : output*x]
        i += 1
    if page != 1:
        a = page - 1
    else:
        a = page
    if page == res:
        b = page
    else:
        b = res - 1
    c = page
    context = {'all_orders':all_orders, 'order_for_page':order_for_page, 'a':a, 'b':b, 'c':c}
    return render(request, 'all_orders.html', context)

def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    form = StatusForm(initial={'status': order.status})
    if request.method == 'POST':
        order.status = request.POST['status']
        order.save()
        return redirect(f'/order_details/{order_id}/')
    context = {'order':order, 'form': form}
    return render(request, 'order_details.html', context)

def order_details_for_buyer(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.status == '?????????????????? ????????????????????':
        products = []
        for i in order.products.all():
            products.append(i)
    else:
        products = None
    context = {'order':order, 'products': products}
    return render(request, 'order_details_for_buyer.html', context)

def rating_product(request,order_id, product_id):
    form = RatingForm()
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        Rating.objects.create(rating=request.POST['rating'], product=product)
        if product.rating == None:
            product.rating = request.POST['rating']
        else:
            count = product.product_rating.count()
            sum = 0
            for i in product.product_rating.all():
                sum += i.rating
            rating = sum/count
            product.rating = round(rating, 1)
        product.save()
        order = Order.objects.get(id=order_id)
        order.status = '?????????????????? ???????????????????? ?? ???????????????? ????????????'
        order.save()
        return redirect('/my_orders/')
    context = {'product':product, 'form':form}
    return render(request, 'rating_product.html', context)

def discount_managment(request):
    form = DiscountForm()
    form_delete = DiscountDeleteForm()
    products = Product.objects.filter(discount=True)
    if request.method == 'POST':
        if request.POST.get('product'):
            products_for_discount = request.POST.getlist('product')
            for product in products_for_discount:
                product = Product.objects.get(id=product)
                product.discount = True
                sale = 1 - int(request.POST.get('discount'))/100
                product.sale = sale
                product.save()
        if request.POST.get('category'):
            category_discount = request.POST.getlist('category')
            for category in category_discount:
                category = Category.objects.get(id=category)
                products = Product.objects.filter(category=category)
                for product in products:
                    product.discount = True
                    sale = 1 - int(request.POST.get('discount')) / 100
                    product.sale = sale
                    product.save()
        if request.POST.get('product_discount'):
            product_discount = request.POST.getlist('product_discount')
            for product in product_discount:
                product = Product.objects.get(id=product)
                product.discount = False
                product.sale = 1
                product.save()

    context = {'products':products, 'form': form, 'form_delete':form_delete}
    return render(request, 'discount_managment.html', context)

def shipping_payment(request):
    return render(request, 'shipping_payment.html')

def discounts(request):
    return render(request, 'discounts.html')



from allauth.account.views import SignupView, LoginView


class MySignupView(SignupView):
    template_name = 'my_signup.html'


class MyLoginView(LoginView):
    template_name = 'my_login.html'