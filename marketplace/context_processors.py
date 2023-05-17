from .models import Cart
def get_counter(request):
    cart_counter=0
    if request.user.is_authenticated:
        try:
            cart_items=Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_counter+=cart_item.quantity
            else:
                cart_counter=0
        except:
            cart_counter=0
        
    
    return dict(cart_counter=cart_counter)

def get_cart_amount(request):
    subTotal=0
    tax=0
    grandTotal=0
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
        if cart_items:
            for cart_item in cart_items:
                subTotal+=cart_item.quantity*cart_item.fooditem.price
        else:
            subTotal=0
            tax=0
            grandTotal=0
        grandTotal=tax+subTotal
    return dict(subTotal=subTotal,tax=tax,grandTotal=grandTotal)
    
       
            


