from django.urls import path,include
from . import views
urlpatterns = [
    path("/",views.marketplace,name="marketplace"),
    path("<slug:slug>",views.vendor_detail,name="vendor_detail"),
    path("add-to-cart/<food_id>",views.add_to_cart,name="add_to_cart"),
    path("remove-from-cart/<food_id>",views.remove_from_cart,name="remove_from_cart")
]
