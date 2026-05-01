from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def customer_list(request):

    customers = Customer.objects.all()

    return render(request, 'customers/customer_list.html', {'customers': customers})


def add_customer(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        Customer.objects.create(
            name=name,
            email=email,
            phone=phone
        )

        messages.success(request, "Customer added successfully!")
        return redirect('/customers/')

    return render(request, 'customers/add_customer.html')


def delete_customer(request, id):

    customer = get_object_or_404(Customer, id=id)

    customer.delete()

    return redirect('/customers/')