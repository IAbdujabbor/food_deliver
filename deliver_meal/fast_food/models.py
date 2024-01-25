from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Food(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foods = models.ManyToManyField(Food, through='OrderItem')
    order_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.pk}"
    def overall_price(self):
        basket_products = self.orderitem_set.all()
        total = sum(order.get_total() for order in basket_products)
        return total

    def product_all_quantity(self):
        basket_products =  self.orderitem_set.all()
        total = sum (order.quantity for order in basket_products)
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)





    def get_total(self):
        return self.food.price * self.quantity





class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=255)
    shipped_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Shipment for Order #{self.order.pk}"
