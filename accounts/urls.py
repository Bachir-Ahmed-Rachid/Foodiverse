
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.myAccount,name='myAccount'),
    path("registerUser",views.userRegister,name='registerUser'),
    path('registerVendor',views.registerVendor,name='registerVendor'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('myAccount',views.myAccount,name='myAccount'),
    path('dashboardCustomer',views.dashboardCustomer,name='dashboardCustomer'),
    path('dashboardVendor',views.dashboardVendor,name='dashboardVendor'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('forget_password',views.forget_password,name='forget_password'),
    path('reset_password',views.reset_password,name='reset_password'),
    path('reset_password_validate/<uidb64>/<token>',views.reset_password_validate,name='reset_password_validate'),
    path('vendor/',include('vendors.urls')),
] 