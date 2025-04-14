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
 path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),


]