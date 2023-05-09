from django.contrib import admin
from .models import Product,Category
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CustomCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=('category_name','vendor','created_at','modified_at')
    search_fields=('category_name','vendor__vendor_name',)

class CustomProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=('product_name','category','vendor','price','is_available','created_at','modified_at',)
    search_fields=('product_name','category__category_name','vendor__vendor_name','price',)
    list_filter=('is_available',)
admin.site.register(Product,CustomProductAdmin)
admin.site.register(Category,CustomCategoryAdmin)