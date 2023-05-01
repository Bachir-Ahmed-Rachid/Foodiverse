from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserForm
from.models import User,UserProfile
from vendors.forms import VendorForm
# Create your views here.

def userRegister(request):
     if request.method=='POST':
          form=UserForm(request.POST)
          if form.is_valid():
               ################
               # METHOD1
               ###############
               #we have to use commit=False so we can add mor abrutîtes to our model
               # password=form.cleaned_data['password']
               # user=form.save(commit=False)
               # user.set_password(password)
               # user.role=User.CUSTOMER
               # user.save()
               ################
               # METHOD2
               ################
               first_name=form.cleaned_data['first_name']
               last_name=form.cleaned_data['last_name']
               username=form.cleaned_data['username']
               phone_number=form.cleaned_data['phone_number']
               email=form.cleaned_data['email']
               password=form.cleaned_data['password']
               user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,phone_number=phone_number,email=email,password=password)
               user.role=User.CUSTOMER
               user.save()
               messages.success(request, 'Your compte has been registered successfully .')
               
               return redirect(userRegister)
          else:
               print(form.errors)
     else:
          form=UserForm()
     context={
     "form":form
     }
     return render(request,'accounts/registerUser.html',context)

def registerVendor(request):
     if request.method=='POST':
          form_user=UserForm(request.POST)
          form_vendor=VendorForm(request.POST,request.FILES)
          if form_user.is_valid() and form_vendor.is_valid():
               first_name=form_user.cleaned_data['first_name']
               last_name=form_user.cleaned_data['last_name']
               username=form_user.cleaned_data['username']
               phone_number=form_user.cleaned_data['phone_number']
               email=form_user.cleaned_data['email']
               password=form_user.cleaned_data['password']
               user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,phone_number=phone_number,email=email,password=password)
               user.role=User.VENDOR
               user.save()
               user_profile=UserProfile.objects.get(user=user)
               vendor=form_vendor.save(commit=False)
               vendor.user=user
               vendor.user_profile=user_profile
               vendor.save()
               messages.success(request, 'Your compte has been registered successfully . Please wait for the approval')
               return redirect(registerVendor)

          else:
               print(form_user.errors)
               print(form_vendor.errors)
     else:
          form_user=UserForm()
          form_vendor=VendorForm()
     context={
     "form_user":form_user,
     "form_vendor":form_vendor,
     }
     return render(request,'accounts/registerVendor.html',context)

