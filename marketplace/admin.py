from django.contrib import admin
from marketplace.models import Cart
from django.contrib.auth.admin import UserAdmin

# Register your models here.
# class CustomCartAdmin(admin.ModelAdmin):
#     list_display =[field.name for field in Cart._meta.fields]

admin.site.register(Cart)