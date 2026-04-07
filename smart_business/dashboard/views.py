from django.shortcuts import render
from products.models import Product
from customers.models import Customer

def dashboard_home(request):

    product_count = Product.objects.count()
    customer_count = Customer.objects.count()

    context = {
        'product_count': product_count,
        'customer_count': customer_count
    }

    return render(request, 'dashboard/dashboard.html', context)