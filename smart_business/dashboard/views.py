from django.shortcuts import render
from products.models import Product
from customers.models import Customer
from orders.models import Order

def dashboard_home(request):

    product_count = Product.objects.count()
    customer_count = Customer.objects.count()
    order_count = Order.objects.count()

    total_sales = sum(order.total_price for order in Order.objects.all())

    context = {
        'product_count': product_count,
        'customer_count': customer_count,
        'order_count': order_count,
        'total_sales': total_sales
    }

    return render(request,'dashboard/dashboard.html',context)