from django import forms
from .models import Category,Product
from accounts.validation import allow_only_images
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']
    


class ProductForm(forms.ModelForm):
    image=forms.FileField(validators=[allow_only_images],widget=forms.FileInput(attrs={'class': 'btn btn-info'},))
    class Meta:
        model = Product
        fields = ['product_name','category','price','image','description','is_available']