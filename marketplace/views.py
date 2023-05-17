from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from marketplace.context_processors import get_cart_amount, get_counter
from marketplace.models import Cart
from menu.models import Category, Product
from django.db.models import Prefetch
from vendors.models import Vendor
from django.contrib.auth.decorators import login_required

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
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
    else:
        cart_items=None
    context={
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items
    }
    return render(request,'marketplace/vendor_detail.html',context)

def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        # check if the request is valid ajax request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # check if the food item exist in our db
            try:
                food_item=Product.objects.get(pk=food_id)
                # check if the user has added this food item in a cart or no
                try:
                    check_cart=Cart.objects.get(user=request.user,fooditem=food_item)
                    check_cart.quantity+=1
                    check_cart.save()
                    return JsonResponse({
                        'status':'success',
                        'message':'Food item was quantity added successfully',
                        'counter':get_counter(request),
                        'cart_amount':get_cart_amount(request),
                        'qty':check_cart.quantity,
                        'id':check_cart.fooditem.pk
                    })
                except:
                    check_cart=Cart.objects.create(user=request.user,fooditem=food_item,quantity=1)
                    check_cart.save()
                    return JsonResponse({
                        'status':'success',
                        'message':'Food item was added successfully to the cart',
                        'counter':get_counter(request),
                        'cart_amount':get_cart_amount(request),
                        'qty':check_cart.quantity,
                        'id':check_cart.fooditem.pk
                        })


            except:
                return JsonResponse({'status':'fail','message':'Food item was not found'})
        else:
            return JsonResponse({'status':'fail','message':'invalide request'})

    else:
        return JsonResponse({'status':'login_required','message':'pleas login to add item to the card'})
    
def remove_from_cart(request,food_id):
    if request.user.is_authenticated:
        # check if the request is valid ajax request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # check if the food item exist in our db
            try:
                food_item=Product.objects.get(pk=food_id)
                # check if the user has added this food item in a cart or no
                try:
                    check_cart=Cart.objects.get(user=request.user,fooditem=food_item)
                    if check_cart.quantity >1:
                        check_cart.quantity-=1
                        check_cart.save()
                        return JsonResponse({
                            'status':'success',
                            'message':'Food item was removed successfully',
                            'counter':get_counter(request),
                            'cart_amount':get_cart_amount(request),
                            'qty':check_cart.quantity,
                            'id':check_cart.fooditem.pk,
                            'id_cart':check_cart.pk
                            })

                    else:
                        deleted_id=check_cart.fooditem.pk
                        check_cart.delete()
                        return JsonResponse({
                            'status':'success',
                            'message':'Cart is empty',
                            'counter':get_counter(request),
                            'cart_amount':get_cart_amount(request),
                            'qty':0,
                            'id':deleted_id
                            })
                except:
                    return JsonResponse({'status':'fail','message':'Cart is already empty'})
            except:
                return JsonResponse({'status':'fail','message':'Food item was not found'})
        else:
            return JsonResponse({'status':'fail','message':'invalide request'})    
    else:
        return JsonResponse({'status':'login_required','message':'pleas login to add item to the card'})
    
@login_required(login_url='login')
def cart(request):

    carts=Cart.objects.filter(user=request.user).order_by('-created_at')
    context={
        'carts':carts
    }

    return render(request,'marketplace/cart.html',context)


def remove_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                cart=Cart.objects.filter(pk=cart_id)
                if cart:
                    cart.delete()
                    return JsonResponse({
                    'status':'success',
                    'message':'Cart is empty',
                    'counter':get_counter(request),
                    'cart_amount':get_cart_amount(request),

                    })
            except:
                return JsonResponse({'status':'fail','message':'Food item was not found'})
        else:
            return JsonResponse({'status':'fail','message':'invalide request'})    
    else:
        return JsonResponse({'status':'login_required','message':'pleas login to remove this card'})

