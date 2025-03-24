"""
URL configuration for fetchandfind project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from store import views
from django.contrib.auth import views as auth_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'cart-items', views.CartItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'discount-codes', views.DiscountCodeViewSet)
router.register(r'admin-logs', views.AdminLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('login/', views.login_view, name='login'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('api/', include(router.urls)),
    #path('api/', include('store.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    #product list
    path('products/', views.product_list, name='product_list'),

    
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
