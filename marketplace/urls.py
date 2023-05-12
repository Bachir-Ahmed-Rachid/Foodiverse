from django.urls import path,include
from . import views
urlpatterns = [
    path("/",views.marketplace,name="marketplace"),
    path("<slug:slug>",views.vendor_detail,name="vendor_detail")
]
