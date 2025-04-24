# admin.py

from django.contrib import admin
from django.contrib.admin.models import LogEntry


from .models import User, Product, CartItem, Order, OrderItem, DiscountCode, AdminLog

admin.site.register(User)
admin.site.register(CartItem)
admin.site.register(OrderItem) # Often better handled as an inline in OrderAdmin
admin.site.register(DiscountCode)
#admin.site.register(AdminLog) # not neccessary
admin.site.register(LogEntry) 



# --- Product Admin Configuration ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'is_on_sale')
    list_filter = ('is_on_sale',)
    search_fields = ('name', 'description')

# --- Order Item Inline Configuration ---
# This allows viewing/editing OrderItems directly within the Order detail page
class OrderItemInline(admin.TabularInline): 
    model = OrderItem
    extra = 0 
    readonly_fields = ('product', 'quantity', 'price_at_purchase', 'subtotal')
    #can_delete = true #false to make it not editable
    def has_add_permission(self, request, obj=None):
        return False

# --- Order Admin Configuration ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date', 'customer_username', 'full_name', 'final_price', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('id', 'user__username', 'full_name', 'address', 'city', 'zip_code', 'checkout_session_id')
    ordering = ('-order_date',)
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'order_date', 'created_at', 'total_price', 'tax', 'discount_applied', 'final_price', 'items', 'checkout_session_id')

    def customer_username(self, obj):
        if obj.user:
            return obj.user.username
        return "N/A"
    customer_username.short_description = 'Customer'
    customer_username.admin_order_field = 'user__username'





#user maintainance

from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model 
from django.conf import settings


User = get_user_model() 

class SessionAdmin(admin.ModelAdmin):
    def session_data_decoded(self, obj):
        return obj.get_decoded()
    session_data_decoded.short_description = 'Session Data (Decoded)'

    def get_user(self, obj):
        session_data = obj.get_decoded()
        user_id = session_data.get('_auth_user_id') 

        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                return user.get_username() 

            except User.DoesNotExist:
                return f"User ID: {user_id} (Deleted)" 
            except Exception as e:
                return f"Error finding user: {e}"
        return "Anonymous" 
    get_user.short_description = 'User' 

    list_display = ['session_key', 'get_user', 'expire_date'] 
    readonly_fields = ['session_key', 'expire_date', 'session_data_decoded', 'get_user']

    ordering = ('-expire_date',)

    search_fields = ['session_key'] 

# Make sure Session is not already registered, or unregister first
try:
    admin.site.unregister(Session)
except admin.sites.NotRegistered:
    pass

admin.site.register(Session, SessionAdmin)