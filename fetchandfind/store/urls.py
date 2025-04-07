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
 path("cart/", views.cart, name="cart"),
 #path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart')


]