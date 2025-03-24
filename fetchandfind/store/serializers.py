from rest_framework import serializers
from .models import User, Product, CartItem, Order, OrderItem, DiscountCode, AdminLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'

class AdminLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminLog
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'image', 'is_on_sale', 'sale_price', 'created_at']