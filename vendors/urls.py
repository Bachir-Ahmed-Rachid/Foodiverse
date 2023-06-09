from django.urls import path
from accounts.views import myAccount 
from . import views 
urlpatterns = [
     path('',myAccount,name='vendor'),
     path('profile/',views.profile,name='vendor_profile'),
     path('menu-builder/',views.menu,name='menu-builder'),
     path('menu-builder/category/add-category',views.add_category,name='add_category'),
     path('menu-builder/category/update-category/<id>',views.update_category,name='update_category'),
     path('menu-builder/category/delete-category/<id>',views.delete_category,name='delete_category'),
     path('menu-builder/category/<id>',views.food_items_by_category,name='food_items_by_category'),

     path('menu-builder/food-item/add-food-item',views.add_food_item,name='add_food_item'),
     path('menu-builder/food-item/update-food-item/<id>',views.update_food_item,name='update_food_item'),
     path('menu-builder/food-item/delete-food-item/<id>',views.delete_food_item,name='delete_food_item'),
    #  path('menu-builder/food-item/<id>',views.food_items_by_food_item,name='food_items_by_food_item'),

 ]
 