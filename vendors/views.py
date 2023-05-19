from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.utils.text import slugify
from .models import Vendor
from accounts.forms import UserProfileForm 
from .forms import VendorForm
from accounts.models import UserProfile
from django.urls import reverse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from accounts.views import is_vendor
from menu.models import Category,Product
from menu.forms import CategoryForm,ProductForm
# Create your views here.


def get_vendor(request):
    return get_object_or_404(Vendor,user=request.user)
@login_required(login_url='login')
@user_passes_test(is_vendor)
def profile(request):
    ##get the vendor and the profileUser from our database
    user_profile = get_object_or_404(UserProfile,user=request.user)
    vendor = get_vendor(request)
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



@login_required(login_url='login')
@user_passes_test(is_vendor)
def menu(request):
    vendor=get_vendor(request)
    categories=Category.objects.filter(vendor=vendor).order_by('-created_at')
    context={
        'categories':categories
    }
    return render(request,'vendors/menu-builder.html',context)


@login_required(login_url='login')
@user_passes_test(is_vendor)
def food_items_by_category(request,id=None):
    category=get_object_or_404(Category,pk=id)
    food_items=Product.objects.filter(category=category)

    context={
        'category':category,
        'food_items':food_items
    }
    return render(request,'vendors/food_items_by_category.html',context)


@login_required(login_url='login')
@user_passes_test(is_vendor)

def add_category(request):
    if request.method=='POST':
        form_category=CategoryForm(request.POST)
        if form_category.is_valid():
            category=form_category.save(commit=False)
            vendor = get_vendor(request)
            category.vendor=vendor
            slug=slugify(form_category.cleaned_data['category_name'])
            category.save()
            category.slug=slug+'_'+str(category.id)
            messages.success(request, 'Category created successfully.')
            return redirect(reverse('add_category'))
        else:
            print(f'{form_category.errors}')
            messages.error(request, 'something went wrong')
    else:
        form_category=CategoryForm()
    context={
        'form_category':form_category
    }
    return render(request,'vendors/add_category.html',context)



@login_required(login_url='login')
@user_passes_test(is_vendor)
def update_category(request,id):
    category=get_object_or_404(Category,pk=id)
    if request.method=='POST':
        form_category=CategoryForm(request.POST,instance=category)
        if form_category.is_valid():
            category=form_category.save(commit=False)
            slug=slugify(form_category.cleaned_data['category_name'])
            category.slug=slug
            category.save()
            messages.success(request, 'Category updated successfully.')
            return redirect(reverse('update_category',args=[id]))
        else:
            print(f'{form_category.errors}')
            messages.error(request, 'something went wrong')
    else:
        form_category=CategoryForm(instance=category)
    context={
        'category':category,
        'form_category':form_category
    }
    return render(request,'vendors/update_category.html',context)


@login_required(login_url='login')
@user_passes_test(is_vendor)
def delete_category(request,id):
    category=get_object_or_404(Category,pk=id)
    category.delete()
    return redirect(reverse('menu-builder'))


@login_required(login_url='login')
@user_passes_test(is_vendor)
def add_food_item(request):
    vendor = get_vendor(request)
    categories=Category.objects.filter(vendor = vendor.pk)
    if request.method == 'POST':
        product_form=ProductForm(request.POST,request.FILES)
        if product_form.is_valid():
            product=product_form.save(commit=False)
            product.vendor=vendor
            slug=slugify(product_form.cleaned_data['product_name'])
            product.slug=slug
            product.save()
            messages.success(request, 'Food Item created successfully.')
            return redirect(reverse('food_items_by_category',args=[product_form.cleaned_data['category'].id]))
        else:
            print(f'{product_form.errors}')
            messages.error(request, 'something went wrong')     
    else:
        
        product_form=ProductForm()
        product_form.fields['category'].queryset=categories
    context={
        'product_form':product_form
    }
    return render(request,'vendors/add_food_item.html',context)






@login_required(login_url='login')
@user_passes_test(is_vendor)
def update_food_item(request,id):
    vendor = get_vendor(request)
    categories=Category.objects.filter(vendor = vendor.pk)
    product=get_object_or_404(Product,pk = id)
    if request.method == 'POST':
        product_form=ProductForm(request.POST,request.FILES,instance=product)
        if product_form.is_valid():
            product=product_form.save(commit=False)
            slug=slugify(product_form.cleaned_data['product_name'])
            product.slug=slug
            product.save()
            messages.success(request, 'Food Item updated successfully.')
            return redirect(reverse('food_items_by_category',args=[product_form.cleaned_data['category'].id]))
        else:
            print(f'{product_form.errors}')
            messages.error(request, 'something went wrong')     
    else:
        
        product_form=ProductForm(instance=product)
        product_form.fields['category'].queryset=categories
    context={
        'product_form':product_form,
        'product':product
    }
    return render(request,'vendors/update_food_item.html',context)



@login_required(login_url='login')
@user_passes_test(is_vendor)
def delete_food_item(request,id):
    product=get_object_or_404(Product,pk=id)
    product.delete()
    return redirect(reverse('menu-builder'))
