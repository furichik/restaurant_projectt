from django.contrib import admin
from auth_system.models import Category, Dish, Order, OrderItem

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(OrderItem)