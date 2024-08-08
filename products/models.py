from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=200)
    price=models.IntegerField()
    description_short = models.CharField(max_length=50)
    description_long = models.TextField()
    size = models.CharField(max_length=50)
    image = models.ImageField(upload_to="product_images", null=True, blank=True)
    options=(
        ('SB', 'Shirts And Blouses'),
        ('TS', 'T-Shirts'),
        ('trending', 'trending'),
        ('HS', 'Hoodies&Sweatshirts'),
        ('men', 'men'),
        ('women', 'women'),
        ('kids', 'kids'),
        ('sports', 'sports'),
        ('tailor', 'tailor'),
        )
    category=models.CharField(max_length=100,choices=options)
    def __str__(self):
        return self.title
    
class Slides(models.Model):
    # ... other fields ...
    image_slide1 = models.ImageField(upload_to="slide_product_images", null=True)
    image_slide2 = models.ImageField(upload_to="slide_product_images", null=True)
    image_slide3 = models.ImageField(upload_to="slide_product_images", null=True)
    
    category = models.CharField(max_length=100, choices=Category.options, default='women')
    
    def __str__(self):
        return "Slide"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} - {self.quantity} x {self.product.price}"

    def total_price(self):
        return self.quantity * self.product.price

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} - {self.user.username}"
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} - {self.quantity} x {self.price}"

class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.address}"
    







    