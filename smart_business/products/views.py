from django.shortcuts import render,redirect,get_object_or_404
from .models import Product, Category
from .forms import ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def product_list(request):

    search = request.GET.get('search')

    if search:
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    return render(request,'products/products_list.html',{'products':products})

def add_product(request):

    form = ProductForm()

    category_id = request.POST.get('category')

    if category_id:
        category = Category.objects.get(id=category_id)
    else:
        category = None

    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")

            return redirect('/products/')
    return render(request,'products/add_products.html',{'form':form})


def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)  # ✅ MUST
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)  # ✅ MUST

    return render(request, 'products/add_products.html', {'form': form})



def delete_product(request,id):

    product = get_object_or_404(Product,id=id)

    product.delete()

    messages.success(request, "Product deleted successfully!")

    return redirect('/products/')


