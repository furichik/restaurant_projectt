from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('like/<int:dish_id>/', views.toggle_like, name='like'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('cart/increase/<str:key>/', views.increase_quantity, name='increase'),
    path('cart/decrease/<str:key>/', views.decrease_quantity, name='decrease'),
    path('cart/remove/<str:key>/', views.remove_from_cart, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
]