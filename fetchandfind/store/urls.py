from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import *
from . import views

app_name = "store"  # This registers the 'store' namespace


urlpatterns = [
 path("", views.home, name="home"),
 path("signup/", authView, name="authView"),
 path("accounts/", include("django.contrib.auth.urls")),
 path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
 path('products/<int:product_id>/', views.product_detail, name='product_detail'),
 path("cart/", views.cart, name="cart"),
 path('user-orders/', views.user_orders, name='user_orders'),
 path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
 path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
 path('checkout/', checkout_view, name='checkout'),

]