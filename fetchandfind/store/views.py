from django.conf import settings
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
from django.db.models import Q
#admin 
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_POST


# Home Page (Requires Login)
def home(request):
    return redirect('/products/') 

@login_required
@require_POST
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
        messages.info(request, "Item was added to the cart.")
        return redirect(request.META.get('HTTP_REFERER', '/products/'))  # Redirect back to the referring page or product list

# Just a slightly modified version of add to cart
@login_required
@require_POST
def buy_now(request, product_id):
    if request.method == "POST":
        try:
            # Fetch the product by its ID
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            # If the product doesn't exist, return an error
            return HttpResponseBadRequest("Product not found")
        
        # Get or create the CartItem for the current user and the selected product
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

        # Get the quantity, default to 1 if not provided
        quantity = int(request.POST.get("quantity", 1))  # Fallback to 1 if not provided
        if quantity <= 0:
            messages.error(request, "Invalid quantity.")
            return redirect("product_detail", product_id=product.id)
    
        # Add quantity if the product already exists in the cart, or set it if it's new
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        # Redirect the user to the cart page after adding the item
        return redirect('cart')  # Replace 'cart' with the actual name of your cart view

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
    # Search both the item name and description   
    search_query = request.GET.get('search')
    if search_query: 
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Handle category filtering (ex: ?category=dogs)
    # Basically just filtering by name and description by searching for the
    # type of category the user clicks on (like cat, dog, food, etc.)
    category = request.GET.get('category')
    if category:
        products = products.filter(
            Q(name__icontains=category) | Q(description__icontains=category)
        )

    # Handle sorting/other filtering
    filter_option = request.GET.get('filter')
    if filter_option == 'price-high':
        products = sorted(products, key=lambda p: p.get_price(), reverse=True)
    elif filter_option == 'price-low':
        products = sorted(products, key=lambda p: p.get_price())
    elif filter_option == 'alpha-asc':
        products = products.order_by('name')
    elif filter_option == 'alpha-desc':
        products = products.order_by('-name')
    elif filter_option == 'quantity-high':
        products = products.order_by('-stock_quantity')
    elif filter_option == 'quantity-low':
        products = products.order_by('stock_quantity')
    

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
def decrememt_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.info(request, "Item quantity decreased.")
    else:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")

    return redirect('cart')

@login_required
@require_POST
def increment_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if cart_item.quantity < cart_item.product.stock_quantity:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, "Item quantity increased.")
    else:
        messages.error(request, "Cannot add more items. Not enough stock available.")
    return redirect('cart')

#delete
@login_required
@require_POST
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')


# Checkout View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
import stripe
from decimal import Decimal
from django.utils import timezone


stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required
def checkout_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_price = sum(item.product.get_price() * item.quantity for item in cart_items)

    if request.method == "POST":
        # Get form data
        full_name = request.POST['full_name']
        address = request.POST['address']
        city = request.POST['city']
        zip_code = request.POST['zip_code']
        discount_code_str = request.POST['discount_code'].upper()

        # Initialize tax, initially assuming no discount is applied
        tax = Decimal(total_price) * Decimal('0.0825')
        # Placeholder for discount logic
        discount_percent = Decimal('0.00')
        discount_decimal = Decimal('0.00')
        discounted_price = Decimal(total_price) # Safer default initialization
        discount_amount = Decimal('0.00')
        
        discount_code_obj = None

        if discount_code_str:
            try:
                discount_code_obj = DiscountCode.objects.get(code=discount_code_str)
                if discount_code_obj.start_date <= timezone.now() <= discount_code_obj.end_date:
                    # Discounts are stored as a percentage (e.g., 1% - 100%)
                    discount_percent = discount_code_obj.discount_value
                    # Convert discount to decimal (e.g., 10% -> 0.1) for calculations
                    discount_decimal = discount_code_obj.discount_value / 100
                    # (e.g., $100 with 10% discount = 100 * (1 - 0.1) = 100 * 0.9 = $90 discounted price)
                    discounted_price = (total_price * (1 - discount_decimal))
                    # (e.g., $100 with 10% discount = 100 * 0.1 = $10 discount)
                    discount_amount = total_price * discount_decimal
                    # Tax collected after discounts
                    tax = discounted_price * Decimal('0.0825')
                    final_price = discounted_price + tax
                    print(f'Discount applied. final price: {final_price} and total price: {total_price}')
                else:
                    messages.error(request, "Discount code is expired or not yet valid.")
                    final_price = total_price + tax
                    print(f'Discount code expired. Final price: {final_price}')
            except DiscountCode.DoesNotExist:
                messages.error(request, "Invalid discount code.")
                final_price = total_price + tax
                print(f'Invalid discount code. Final price: {final_price}')
        else:
            final_price = total_price + tax

        # Save order data in session temporarily
        request.session['order_data'] = {
            'full_name': full_name,
            'address': address,
            'city': city,
            'zip_code': zip_code,
            'total_price': str(total_price),
            'tax': str(tax),
            'discount': str(discount_percent),
            'final_price': str(final_price),
            'discounted_price': str(discounted_price),
            'discount_amount': str(discount_amount),
        }

        # Build line items for Stripe
        line_items = [{
            'price_data': {
                'currency': 'usd',
                # Apply the discount to each line item to send to Stripe
                'unit_amount': int((item.product.get_price() * (1 - discount_decimal)) * 100),  # convert to cents
                'product_data': {
                    'name': item.product.name,
                },
            },
            'quantity': item.quantity,
        } for item in cart_items]

        # Add discount as a separate line item with a price of $0.00
        if discount_amount > 0:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 0,  # no charge for discount, set to 0
                    'product_data': {
                        'name': f"{discount_percent}% off order. Discount has already been applied per line item.",
                    },
                },
                'quantity': 1,
            })

        # If user entered a discount code and it was invalid or expired, send $0.00 line item to Stripe
        if discount_amount == 0 and discount_code_str:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 0,  # no charge for invalid discount
                    'product_data': {
                        'name': "Discount code was invalid or expired. No discount was applied.",
                    },
                },
                'quantity': 1,
            })

        # Add tax as a separate line item. Tax already accounts for potential discount
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(tax * 100),  # convert tax to cents
                'product_data': {
                    'name': 'Sales Tax (8.25%)',
                },
            },
            'quantity': 1,
        })

        # Create Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/user-orders/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/checkout/'),
        )

        # Store the cart item info in the session too
        request.session['cart_items'] = [
            {'product_id': item.product.id, 'quantity': item.quantity}
            for item in cart_items
        ]

        return redirect(session.url, code=303)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

#logs admin actions
@login_required
def log_admin_action(admin_user, action_text):
    AdminLog.objects.create(admin=admin_user, action=action_text)


@login_required
def user_orders(request):
    session_id = request.GET.get('session_id')

    # Initialize context and discount_percentage variables
    context = {
        'orders': Order.objects.filter(user=request.user).prefetch_related('orderitem_set').order_by('-order_date'),
    }

    if session_id and 'order_data' in request.session and 'cart_items' in request.session:
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':
            order_data = request.session.pop('order_data', None)
            cart_data = request.session.pop('cart_items', None)

            if order_data and cart_data:
                # Prevent duplicate order creation for same session
                existing_order = Order.objects.filter(checkout_session_id=session_id).exists()
                if not existing_order:
                    order = Order.objects.create(
                        user=request.user,
                        full_name=order_data['full_name'],
                        address=order_data['address'],
                        city=order_data['city'],
                        zip_code=order_data['zip_code'],
                        total_price=Decimal(order_data['total_price']),
                        tax=Decimal(order_data['tax']),
                        discount_applied=Decimal(order_data['discount']),
                        final_price=Decimal(order_data['final_price']),
                        discounted_price=Decimal(order_data['discounted_price']),
                        discount_amount=Decimal(order_data['discount_amount']),
                        status='pending',
                        checkout_session_id=session_id
                    )

                    for item in cart_data:
                        product = Product.objects.get(id=item['product_id'])
                        
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item['quantity'],
                            price_at_purchase=product.get_price(),
                            subtotal=product.get_price() * item['quantity']
                        )

                        # Decrease product's stock quantity
                        product.stock_quantity -= item['quantity']
                        product.save()

                    # Clear cart after order creation
                    CartItem.objects.filter(user=request.user).delete()

    return render(request, 'user_orders.html', context)


# Cancel an order
@login_required
@require_POST
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'pending':
        # Restock each product
        # Get all orderitems belonging to order
        order_items = order.orderitem_set.all()
        for item in order_items:
            # Get the product associated with an order_item
            product = item.product
            # Increase the product's stock by the order_item's quantity
            product.stock_quantity += item.quantity
            product.save()

        # Update the order's status
        order.status = 'canceled'
        order.save()
        messages.success(request, "Order was successfully canceled.")

    return redirect('store:user_orders')


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