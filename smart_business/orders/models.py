from django.db import models
from customers.models import Customer
from products.models import Product
from datetime import date

class Order(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    # ✅ ADD THIS
    def total_price(self):
        return self.product.price * self.quantity