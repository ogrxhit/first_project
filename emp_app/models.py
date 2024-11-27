from django.db import models
from django.contrib.auth.models import User

# User Profile extension (if you need to add extra fields to the default User model)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'ecommerce_user_profile'  # Custom table name

    def __str__(self):
        return self.user.username

# Product Table
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'ecommerce_product'

    def __str__(self):
        return self.name

# Category Table
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description provided")

    class Meta:
        db_table = 'ecommerce_category'

    def __str__(self):
        return self.name

# Cart Table
class Cart(models.Model):
    user = models.ForeignKey(User, related_name='carts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ecommerce_cart'

    def __str__(self):
        return f"Cart of {self.user.username}"

# CartItem Table
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'ecommerce_cart_item'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# Order Table
class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    shipping_address = models.ForeignKey('ShippingAddress', related_name='orders', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ecommerce_order'

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# OrderItem Table
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'ecommerce_order_item'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# ShippingAddress Table
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, related_name='shipping_addresses', on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'ecommerce_shipping_address'

    def __str__(self):
        return f"{self.address_line_1}, {self.city}"

# Payment Table
class Payment(models.Model):
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), ('PayPal', 'PayPal'), ('Bank Transfer', 'Bank Transfer')])
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ecommerce_payment'

    def __str__(self):
        return f"Payment for Order {self.order.id}"
