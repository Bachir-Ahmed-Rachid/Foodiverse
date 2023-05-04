from django.urls import path
from accounts.views import myAccount 
from . import views 

urlpatterns = [
     path('',myAccount,name='vendor'),
     path('profile/',views.profile,name='vendor_profile'),

 ]
 