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
from django.views.decorators.http import require_POST


# Home Page (Requires Login)
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
        return redirect(request.META.get('HTTP_REFERER', '/products/'))  # Redirect back to the referring page or product list


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
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.get_subtotal() for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal
    })

#delete cart item
@login_required
@require_POST
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.info(request, "Item quantity decreased.")
    else:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")

    return redirect('cart')



#logs admin actions
def log_admin_action(admin_user, action_text):
    AdminLog.objects.create(admin=admin_user, action=action_text)


# View the user's orders
@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'user_orders.html', {'orders': orders})


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