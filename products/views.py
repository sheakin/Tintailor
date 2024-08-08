from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Sum, F
from .models import Category, Cart, CartItem, Order, OrderItem, Slides,WishlistItem
from .forms import CartItemForm
from django.contrib.auth.decorators import login_required

class HomeView(TemplateView):
    template_name = "home.html"


class ProductView(ListView):
    template_name = "products.html"
    context_object_name = "data"

    def get_queryset(self):
        category = self.kwargs.get('cat', 'all')
        if category == 'all':
            return Category.objects.all()
        return Category.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('cat', 'all')
        if category == 'all':
            context['slides'] = Slides.objects.first()
        else:
            context['slides'] = Slides.objects.filter(category=category).first()
        context['category'] = category  
        return context
class ProductDetailView(DetailView):
    template_name = "details.html"
    model = Category
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = Category.objects.all()
        return context

# Cart view
def cart_view(request):
    cart_items, total_price = [], 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, active=True)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = cart_items.aggregate(total_price=Sum(F('quantity') * F('product__price')))['total_price'] or 0

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Add item to cart
def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return redirect('login') 

    product = get_object_or_404(Category, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user, active=True)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')

# Remove item from cart
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('cart_view')

# Update cart item
def update_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('cart_view')
    else:
        form = CartItemForm(instance=cart_item)

    return render(request, 'update_cart_item.html', {'form': form})

#wishing list

@login_required
def Wishlist_view(request):
    user = request.user
    wishlist_items = WishlistItem.objects.filter(user=user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist.html', context)

@login_required
def add_to_wishlist(request, pk):
    product = get_object_or_404(Category, pk=pk)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        wishlist_item.quantity += 1
        wishlist_item.save()

    print(f"Added {product.title} to wishlist for user {request.user.username}")
    return redirect('wishlist_view')


# Checkout view
def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    cart = Cart.objects.filter(user=request.user, active=True).first()
    if not cart:
        return redirect('cart_view')  

    cart_items = CartItem.objects.filter(cart=cart)
    total_price = cart_items.aggregate(total_price=Sum(F('quantity') * F('product__price')))['total_price'] or 0
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

# aggregate: This is a queryset method that computes a summary value over the entire queryset. 
    # In this case, it is used to calculate the total price of all items in the cart.

    # F: This is a Django function used to refer to model field values directly in expressions and queries. 
    # It allows you to perform operations involving model fields without fetching their values 

# Place order view
def place_order(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  

        cart = Cart.objects.filter(user=request.user, active=True).first()
        if not cart:
            return redirect('cart_view')  
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = cart_items.aggregate(total_price=Sum(F('quantity') * F('product__price')))['total_price'] or 0
        order = Order.objects.create(user=request.user, cart=cart, total_price=total_price)       
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)    
        cart.active = False
        cart.save()

        return redirect('order_success', order_id=order.id)

    return redirect('checkout_view')

# Order success view
def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_success.html', {'order': order})




# Order details view
def order_details(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_details.html', {'order': order, 'order_items': order_items})




