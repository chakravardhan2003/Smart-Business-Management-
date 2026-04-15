from django.shortcuts import render,redirect,get_object_or_404
from .models import Product
from .forms import ProductForm

def product_list(request):

    search = request.GET.get('search')

    if search:
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    return render(request,'products/products_list.html',{'products':products})

def add_product(request):

    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/products/')

    return render(request,'products/add_products.html',{'form':form})


def edit_product(request,id):

    product = get_object_or_404(Product,id=id)

    form = ProductForm(instance=product)

    if request.method == "POST":
        form = ProductForm(request.POST,instance=product)

        if form.is_valid():
            form.save()
            return redirect('/products/')

    return render(request,'products/add_products.html',{'form':form})

def delete_product(request,id):

    product = get_object_or_404(Product,id=id)

    product.delete()

    return redirect('/products/')