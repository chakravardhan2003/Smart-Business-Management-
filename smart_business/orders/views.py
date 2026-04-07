from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from customers.models import Customer
from products.models import Product


def order_list(request):

    orders = Order.objects.all()

    return render(request, 'orders/orders_list.html', {'orders': orders})


def add_order(request):

    customers = Customer.objects.all()
    products = Product.objects.all()

    if request.method == "POST":

        customer_id = request.POST.get('customer')
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))

        customer = Customer.objects.get(id=customer_id)
        product = Product.objects.get(id=product_id)

        total_price = product.price * quantity

        Order.objects.create(
            customer=customer,
            product=product,
            quantity=quantity,
            total_price=total_price
        )

        return redirect('/orders/')

    context = {
        'customers': customers,
        'products': products
    }

    return render(request, 'orders/add_order.html', context)


def delete_order(request, id):

    order = get_object_or_404(Order, id=id)

    order.delete()

    return redirect('/orders/')