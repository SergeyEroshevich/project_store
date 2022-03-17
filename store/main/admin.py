from django.contrib import admin

from .models import Category, Product, Brand, Image


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated','description']
    list_filter = ['available', 'created', 'updated', 'price']
    list_editable = ['price', 'stock', 'available','description']


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Image)
