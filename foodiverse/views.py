from django.shortcuts import render
from django.http import HttpResponse

from vendors.models import Vendor
def home(request):
     vendors=Vendor.objects.filter(user__is_active=True,is_approved=True)[:8]
     context={
          'vendors':vendors
     }
     return render(request,'home.html',context)
