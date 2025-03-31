from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm



# Create your views here.
@login_required
def home(request):
    template_n = loader.get_template('home.html')
    return HttpResponse(template_n.render())

def login(request):
    template_n = loader.get_template('login.html')
    return HttpResponse(template_n.render())


def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("registration/login.html")
 else:
  form = UserCreationForm()
 return render(request, "registration/signup.html", {"form": form})

def logout(request):
    template_n = loader.get_template('logout.html')
    return HttpResponse(template_n.render())

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')  # Redirect to the home page (or any other view)
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()  # Query all products
    return render(request, 'product_list.html', {'products': products})


from rest_framework import viewsets
from .models import User, Product, CartItem, Order, OrderItem, DiscountCode, AdminLog
from .serializers import UserSerializer, ProductSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer, DiscountCodeSerializer, AdminLogSerializer

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