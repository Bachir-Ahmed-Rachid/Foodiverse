from django import forms
from .models import Vendor
from accounts.validation import allow_only_images
class VendorForm(forms.ModelForm):
    vendor_licence=forms.FileField(validators=[allow_only_images],widget=forms.FileInput(attrs={'class': 'btn btn-info'},))

    class Meta:
        model=Vendor
        fields=['vendor_name','vendor_licence']
