from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Vendor
from accounts.forms import UserProfileForm 
from .forms import VendorForm
from accounts.models import UserProfile
from django.urls import reverse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from accounts.views import is_vendor

# Create your views here.
@login_required(login_url='login')
@user_passes_test(is_vendor)
def profile(request):
    ##get the vendor and the profileUser from our database
    user_profile = get_object_or_404(UserProfile,user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)
    if request.method == 'POST':
        form_vendor = VendorForm(request.POST,request.FILES,instance=vendor)
        form_user_profile = UserProfileForm(request.POST,request.FILES,instance=user_profile)

        if form_vendor.is_valid() and form_user_profile.is_valid():
            vendor=form_vendor.save()
            user_profile=form_user_profile.save()
            messages.success(request, 'Updated successfully.')
            return redirect(reverse('vendor_profile'))
        else:
            print(f'{form_user_profile.errors},{form_vendor.errors}')
            messages.error(request, 'something went wrong')
            # return redirect(reverse('vendor_profile'))
    else:
        #creating instance of th forms to extract existing data
        form_user_profile=UserProfileForm(instance=user_profile)
        form_vendor=VendorForm(instance=vendor)

    context={
        'form_user_profile':form_user_profile,
        'form_vendor':form_vendor,

    }
    return render(request,'vendors/profile.html',context)
