from django.template.context_processors import static
from django.urls import path
from django.contrib.auth.views import LogoutView

from food_del import settings
from .views import *

urlpatterns = [
 
    path('', base_foods, name='base_foods'),
    path('add_to_basket/<int:food_id>/', add_to_basket, name='add_to_basket'),
    path('navbar/', navbar, name='navbar'),


    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('change_quantity/<int:item_id1>/<int:change1>/', change_quantity, name='change_quantity'),
    path('decrase_quantity/<int:item_id>/<int:change>/', decrase_quantity, name='decrase_quantity'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
    path('create_shipment/<int:order_id>/', create_shipment, name='create_shipment'),
    path('orders/<int:order_id>/shipment/', shipment_detail, name='shipment_detail'),
    path('admin_order_list/', admin_order_list, name='admin_order_list'),
    path('admin_order_detail/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
    path('admin_shipment_detail/<int:order_id>/shipment/', admin_shipment_detail, name='admin_shipment_detail'),
    #url for login
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin_main_page/', admin_main_page, name='admin_main_page'),
]
    # Add other URL patterns as needed

