
from django.urls import path
from . import views

urlpatterns = [
    path("registerUser",views.userRegister,name='registerUser'),
    path('registerVendor',views.registerVendor,name='registerVendor'),
] 