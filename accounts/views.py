from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .forms import UserForm
from.models import User,UserProfile
from vendors.forms import VendorForm
from django.contrib import auth 
from django.contrib.auth.decorators import login_required,user_passes_test
from .utils import get_redirect_url,send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
# Create your views here.


def is_vendor(user):
     if user.role == 1:
          return True
     else:
          raise PermissionDenied("You are not authorized to access this page.")
     
def is_customer(user):
     if user.role == 2:
          return True
     else:
          raise PermissionDenied("You are not authorized to access this page.")
     
def userRegister(request):
     if request.user.is_authenticated:
          messages.info(request, 'You are already logged in.')
          return redirect('myAccount')
     elif request.method=='POST':
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
               send_verification_email(request,user,'Account activation','accounts/emails/account_verification_email.html')
               messages.success(request, 'Your compte has been registered successfully . Please wait for the approval')
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
     if request.user.is_authenticated:
          messages.info(request, 'You are already logged in.')
          return redirect('myAccount')

     elif request.method=='POST':
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
               send_verification_email(request,user,'Account activation','accounts/emails/account_verification_email.html')
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


def login(request):
     if request.user.is_authenticated:
          messages.info(request, 'You are already logged in.')
          return redirect('myAccount')
     elif(request.method=='POST'):
          email=request.POST['email']
          password=request.POST['password']
          user = auth.authenticate(email=email, password=password)
          if user is not None:
               auth.login(request,user)
               messages.success(request, 'Successfully logged in.')
               return redirect('myAccount')

          else:
               messages.error(request, 'Invalid login details')
               return redirect('login')
     return render(request,'accounts/login.html')
def logout(request):
     auth.logout(request)
     messages.info(request, 'Successfully logged out.')
     return redirect('login')

@login_required(login_url='login')
def myAccount(request):
     redirect_url=get_redirect_url(request.user)
     return redirect(redirect_url)

@login_required(login_url='login')
@user_passes_test(is_vendor)
def dashboardVendor(request):
     return render(request,'accounts/dashboard_vendor.html')

@login_required(login_url='login')
@user_passes_test(is_customer)

def dashboardCustomer(request):
     return render(request,'accounts/dashboard_customer.html')

def activate(request,uidb64,token):
     try:
          uid=urlsafe_base64_decode(uidb64).decode()
          user=User._default_manager.get(pk=uid)
     except:
          user=None

     if user is not None and  default_token_generator.check_token(user,token):
          user.is_active=True
          user.save()
          messages.success(request, 'Congratulation your account is activated.')
          return redirect('myAccount')
     else:
          messages.error(request, 'Invalid activation link.')
          return redirect('myAccount')
             

def forget_password(request):
     if request.method == 'POST':
          email=request.POST['email']
          if User.objects.filter(email=email).exists():
               user=User.objects.get(email__exact=email)
               ##Send the message
               send_verification_email(request,user,'Password reset','accounts/emails/account_reset_password.html')
               messages.success(request, 'Verification link has been sent to your mail inbox.')
               return redirect('forget_password')
          else:
               messages.error(request, 'Invalid email address.')
               return redirect('forget_password')

     return render(request,'accounts/forget_password.html')

def reset_password_validate(request,uidb64,token):
     try:
          uid=urlsafe_base64_decode(uidb64).decode()
          user=User._default_manager.get(pk=uid)
     except:
          user=None

     if user is not None and  default_token_generator.check_token(user,token):
          request.session['uid']=uid
          messages.info(request, 'Please insert and confirme your new password.')
          return redirect('reset_password')
     else:
          messages.error(request, 'Invalid reset password link.')
          return redirect('myAccount')

def reset_password(request):
     if request.method =='POST':
          print(request.POST)
          password=request.POST['password']
          password_confirm=request.POST['password_confirm']
          
          if password == password_confirm:
               pk=request.session.get('uid')
               user=User.objects.get(pk=pk)
               user.set_password(password)
               user.save()
               messages.success(request, 'Password modified successfully')
               return redirect('login')
          else:
               messages.error(request, "Passwords did't match.")
               return redirect('reset_password')
     return render(request,'accounts/reset_password.html')
