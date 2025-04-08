from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=150)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    user_role = models.CharField(max_length=10, choices=[('customer', 'Customer'), ('admin', 'Admin')])
    created_at = models.DateTimeField(auto_now_add=True)

    # Set related_name to avoid clashing with the auth.User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='store_user_set',  # Modify the related_name to avoid clashing
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='store_user_permissions_set',  # Modify the related_name to avoid clashing
        blank=True,
    )
# Product Model
class Product(models.Model):
    name = models.CharField(max_length=252)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Add a name for the image field
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Returns the sale price if the product is on sale, 
    # otherwise returns the regular price.
    # Should be used during checkout, not on product_detail page 
    # (Keeping discounts soley tied to coupons, for simplicity)
    def get_price(self):
        if self.is_on_sale and self.sale_price:
            return self.sale_price
        return self.price
# Shopping Cart Model
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

# Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('canceled', 'Canceled')])
    order_date = models.DateTimeField(auto_now_add=True)

# Order Items Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

# Discount Code Model
class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_role': 'admin'})
    created_at = models.DateTimeField(auto_now_add=True)

# Admin Log Model
class AdminLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_role': 'admin'})
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    
