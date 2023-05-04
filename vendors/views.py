from django.shortcuts import render
from django.http import HttpResponse
from .models import Vendor
# Create your views here.

def profile(request):
    return render(request,'vendors/profile.html')
