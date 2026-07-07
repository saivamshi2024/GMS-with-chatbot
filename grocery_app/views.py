from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .chatbot import get_chatbot_response

def payment(request):
    """View for the Payment page"""
    order_id = request.GET.get('order_id')
    if not order_id:
        messages.error(request, 'No order to pay for.')
        return redirect('grocery_app:view_cart')
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        # Here you would handle payment logic and validation
        # For now, just show a success message or redirect
        messages.success(request, 'Payment option selected! (Demo only)')
        # Clear cart after payment
        request.session['cart'] = {}
        return redirect('grocery_app:order_confirmation', order_id=order.id)
    return render(request, 'grocery_app/payment.html', {'title': 'Payment', 'order': order})
def about(request):
    """View for the About page"""
    return render(request, 'grocery_app/about.html', {'title': 'About Us'})
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderItem
from django.core.paginator import Paginator

def home(request):
    """Home page view showing featured products and categories"""
    categories = Category.objects.all()
    featured_products = Product.objects.filter(stock__gt=0).order_by('-created_at')[:6]
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'title': 'Groceries Made Easy'
    }
    return render(request, 'grocery_app/home.html', context)

def product_list(request):
    """View for listing all products with filtering and search"""
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort', 'name')  # Default sort by name
    
    # Start with all products
    products = Product.objects.all()
    
    # Apply category filter
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Apply search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Apply sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:  # default to name
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    context = {
        'products': products_page,
        'categories': categories,
        'current_category': category_id,
        'search_query': search_query,
        'sort_by': sort_by,
        'title': 'Our Products'
    }
    return render(request, 'grocery_app/product_list.html', context)

def product_detail(request, product_id):
    """View for showing product details"""
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product_id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'title': product.name
    }
    return render(request, 'grocery_app/product_detail.html', context)

def category_detail(request, category_id):
    """View for showing products in a specific category"""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': products_page,
        'title': category.name
    }
    return render(request, 'grocery_app/category_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    """View for adding products to cart"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Get or create cart in session
        cart = request.session.get('cart', {})
        
        # Add or update product in cart
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += quantity
        else:
            cart[str(product_id)] = {
                'quantity': quantity,
                'price': str(product.price),
                'name': product.name
            }
        
        request.session['cart'] = cart
        messages.success(request, f'Added {quantity} {product.name} to cart')
        
        return redirect('grocery_app:product_detail', product_id=product_id)
    return redirect('grocery_app:product_list')

@login_required
def view_cart(request):
    """View for showing cart contents"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item['quantity']
        price = float(item['price'])
        subtotal = quantity * price
        
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal
        })
        total += subtotal
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'title': 'Shopping Cart'
    }
    return render(request, 'grocery_app/cart.html', context)

@login_required
def checkout(request):
    """View for processing checkout"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, 'Your cart is empty')
            return redirect('grocery_app:view_cart')
        
        # Create order
        order = Order.objects.create(
            customer_name=request.user.get_full_name() or request.user.username,
            customer_email=request.user.email,
            status='pending',
            total_amount=sum(
                float(item['price']) * item['quantity']
                for item in cart.values()
            )
        )
        
        # Create order items
        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )
            
            # Update product stock
            product.stock -= item['quantity']
            product.save()
        
        # Do not clear cart or show success yet; redirect to payment
        return redirect(f"{reverse('grocery_app:payment')}?order_id={order.id}")
    
    return render(request, 'grocery_app/checkout.html', {
        'title': 'Checkout'
    })

@login_required
def order_confirmation(request, order_id):
    """View for showing order confirmation"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'title': f'Order #{order.id} Confirmation'
    }
    return render(request, 'grocery_app/order_confirmation.html', context)

@csrf_exempt
def chat_api(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required"},
            status=405
        )

    try:

        data = json.loads(request.body)

        message = data.get("message", "")

        answer = get_chatbot_response(message)

        return JsonResponse({
            "reply": answer
        })

    except Exception as e:

        return JsonResponse({
            "reply": str(e)
        })
