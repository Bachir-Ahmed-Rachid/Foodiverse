
from django.urls import path
from . import views

urlpatterns = [
    path("registerUser",views.userRegister,name='registerUser'),
    path('registerVendor',views.registerVendor,name='registerVendor'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('myAccount',views.myAccount,name='myAccount'),
    path('dashboardCustomer',views.dashboardCustomer,name='dashboardCustomer'),
    path('dashboardVendor',views.dashboardVendor,name='dashboardVendor'),
] 