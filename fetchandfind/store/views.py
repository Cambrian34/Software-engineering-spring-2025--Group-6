from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseBadRequest
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product
from rest_framework import viewsets
from .serializers import UserSerializer, ProductSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer, DiscountCodeSerializer, AdminLogSerializer
from .models import User, Product, CartItem, Order, OrderItem, DiscountCode, AdminLog
#admin 
from .forms import CustomUserCreationForm


# Home Page (Requires Login)
@login_required
def home(request):
    return redirect('/products/') 

@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponseBadRequest("Product not found")
        
        # Get or create the CartItem for the current user
        # Ensure that 'user=request.user' is properly passed to associate it with the logged-in user
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

        quantity = int(request.POST.get("quantity", 1))  # Fallback to 1 if not provided
        if quantity <= 0:
            messages.error(request, "Invalid quantity.")
            return redirect("product_detail", product_id=product.id)
    
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
        cart_item.save()
        return redirect('/products/')  # Redirect to the product list or cart page
    return redirect('/products/') 


# Signup View
def authView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to login after signup
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# Logout View 
def logout_view(request):
    logout(request)
    return redirect("login")

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

# Product List View
def product_list(request):
    products = Product.objects.all()

    # Handle search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Handle filtering
    filter_option = request.GET.get('filter')
    if filter_option == 'price-high':
        products = products.order_by('-price')
    elif filter_option == 'price-low':
        products = products.order_by('price')
    

    return render(request, 'product_list.html', {'products': products})
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

#Cart View
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.get_subtotal() for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal
    })



#logs admin actions
def log_admin_action(admin_user, action_text):
    AdminLog.objects.create(admin=admin_user, action=action_text)
# Django REST Framework ViewSets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class DiscountCodeViewSet(viewsets.ModelViewSet):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer

class AdminLogViewSet(viewsets.ModelViewSet):
    queryset = AdminLog.objects.all()
    serializer_class = AdminLogSerializer