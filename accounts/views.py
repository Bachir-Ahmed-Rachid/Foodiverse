from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserForm
from.models import User
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
               messages.success(request, 'Your compte has been registered successfully .')
               user.save()
               
               return redirect(userRegister)
          else:
               print(form.errors)
     else:
          form=UserForm()
     context={
     "form":form
     }
     return render(request,'accounts/registerUser.html',context)
