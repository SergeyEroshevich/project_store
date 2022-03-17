from django import forms
from django.contrib.auth.models import User

from .models import Product, Brand, Profile, Category, Order, Rating


class ProductForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Наименование')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория')
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label='Бренд')
    price = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0, label='Стоимость')
    country = forms.CharField(max_length=30, label='Страна производства')
    description = forms.CharField(max_length=100, label='Краткое описание', widget=forms.Textarea)
    full_description = forms.CharField(max_length=250, label='Подробное описание', widget=forms.Textarea)
    stock = forms.IntegerField(min_value=0, label='Количество')

    class Meta:
        model = Product
        fields = ('name', 'category', 'brand','price','country','description','full_description','stock')

class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=30, label='Логин')
    password = forms.CharField(max_length=30, label='Пароль', widget=forms.PasswordInput())

    class Meta:
        model = Profile
        fields = ('username', 'password')

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, label='Логин')
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    password = forms.CharField(max_length=30, label='Пароль', widget=forms.PasswordInput())
    email = forms.EmailField(label='Электронная почта')
    phone = forms.IntegerField(label='Телефон')
    adress = forms.CharField(max_length=100, label='Адрес', widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'phone', 'adress')


class ChangeUserlnfoForm(forms.ModelForm):
    adress = forms.CharField(widget=forms.Textarea, label='Адрес')
    phone = forms.IntegerField( label='Телефон')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)

class OrderForm(forms.ModelForm):
    adress = forms.CharField(widget=forms.Textarea())
    phone = forms.CharField(widget=forms.TextInput())
    total = forms.CharField(label= 'Итого', widget=forms.TextInput(attrs={'readonly':'readonly'}))


    class Meta:
        model = Order
        fields = ('phone', 'adress', 'payment', 'delivery', 'comment', 'total')

class SortForm(forms.Form):
    CHOICES = ((1, 'по убыванию цены'), (2, 'по возрастанию цены'), (3, 'по популярности'), (4, 'по рейтингу'), (5, 'новые'))
    sort = forms.ChoiceField(choices=CHOICES, label='Сортировать')

class StatusForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('status',)

class RatingForm(forms.ModelForm):
    CHOICES = ((1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10))
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label='Оценка')

    class Meta:
        model = Rating
        fields = ('rating',)


class SearchForm(forms.Form):
    discount = forms.BooleanField(label='Товары со скидкой')
    brand = forms.ModelMultipleChoiceField(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple, label='Производитель')
    price_from = forms.IntegerField(min_value=0, label='стоимость от')
    price_to = forms.IntegerField(min_value=0, label='стоимость до')