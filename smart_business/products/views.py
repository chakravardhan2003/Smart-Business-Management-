from django.shortcuts import render,redirect,get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/products_list.html', {'products': products})


def add_product(request):

    if request.method == "POST":

        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        Product.objects.create(
            name=name,
            price=price,
            quantity=quantity
        )

        return redirect('/products/')

    return render(request, 'products/add_products.html')


def delete_product(request, id):

    product = get_object_or_404(Product, id=id)

    product.delete()

    return redirect('/products/')
