from django.shortcuts import get_list_or_404, get_object_or_404, render
from menu.models import Category, Product
from django.db.models import Prefetch
from vendors.models import Vendor

# Create your views here.
def marketplace(request):
    vendors=Vendor.objects.filter(user__is_active=True,is_approved=True)
    vender_count=vendors.count()
    context={
        'vendors':vendors,
        'vender_count':vender_count
    }
    return render(request,'marketplace/listings.html',context)

def vendor_detail(request,slug):
    vendor=get_object_or_404(Vendor,slug=slug)
    categories=Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'product',
            queryset=Product.objects.filter(is_available=True)
        )
    )
    print(categories)
    context={
        'vendor':vendor,
        'categories':categories
    }
    return render(request,'marketplace/vendor_detail.html',context)