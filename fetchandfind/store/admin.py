from django.contrib import admin
from django.contrib.admin.models import LogEntry


# Register your models here.
from .models import User, Product, CartItem, Order, OrderItem, DiscountCode, AdminLog

admin.site.register(User)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DiscountCode)
admin.site.register(AdminLog)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'is_on_sale')






