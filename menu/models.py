from django.db import models
from vendors.models import Vendor
# Create your models here.

class Category(models.Model):
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    category_name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=250,blank=True)
    created_at=models.DateField(auto_now_add=True)
    modified_at=models.DateField(auto_now=True)
    class Meta:
        verbose_name="category"
        verbose_name_plural="categories"

    def clean(self):
        self.category_name = self.category_name.capitalize()    
        return self.category_name
    def __str__(self):
        return self.category_name


class Product(models.Model):
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='product')
    product_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='foodImages',blank=True,null=True)
    description=models.TextField(max_length=250,blank=True)
    is_available=models.BooleanField(default=True)
    created_at=models.DateField(auto_now_add=True)
    modified_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.product_name