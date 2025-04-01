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
    path("", views.home, name="home"),  # This registers 'home' as a valid route

    
    # Authentication views
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("signup/", views.authView, name="signup"),
    path('products/', views.product_list, name='product_list'), 

    # API routes
    path('api/', include(router.urls)),

    # Store URLs
    path("", include("store.urls")),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)