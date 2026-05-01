from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from customers.models import Customer
from products.models import Product
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.core.mail import EmailMessage
from django.conf import settings
import json
from django.db import transaction
from django.contrib.auth.decorators import login_required


# ==============================
# SEND INVOICE EMAIL (HTML → PDF)
# ==============================
def send_invoice_email(order):
    template = get_template('orders/invoice.html')
    html = template.render({'order': order})

    buffer = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=buffer)

    pdf = buffer.getvalue()
    buffer.close()

    email = EmailMessage(
        subject=f"Invoice #{order.id}",
        body=f"""
Dear {order.customer.name},

Thank you for your order.

Please find your invoice attached.

Regards,  
Inventra Team
""",
        from_email=settings.EMAIL_HOST_USER,
        to=[order.customer.email],
    )

    email.attach(f"invoice_{order.id}.pdf", pdf, 'application/pdf')
    email.send()


# ==============================
# GENERATE PDF (DOWNLOAD)
# ==============================
def invoice_pdf(request, id):
    order = get_object_or_404(Order, id=id)

    template = get_template('orders/invoice.html')
    html = template.render({'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=response
    )

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response


# ==============================
# VIEW INVOICE (HTML)
# ==============================
def invoice_view(request, id):
    order = get_object_or_404(Order, id=id)

    return render(request, 'orders/invoice.html', {
        'order': order
    })

# ==============================
# ORDER LIST
# ==============================
def order_list(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'orders/orders_list.html', {'orders': orders})


# ==============================
# ADD ORDER (MULTIPLE PRODUCTS)
# ==============================


def add_order(request):

    customers = Customer.objects.all()
    products = Product.objects.all()

    import json
    products_json = json.dumps({
        str(p.id): {
            "price": float(p.price),
            "stock": p.quantity
        }
        for p in products
    })

    if request.method == "POST":

        customer_id = request.POST.get('customer')
        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')

        if not customer_id:
            messages.error(request, "Please select customer")
            return redirect('add_order')

        customer = Customer.objects.get(id=customer_id)

        # =========================
        # ✅ STEP 1: VALIDATE STOCK FIRST
        # =========================
        for product_id, qty in zip(product_ids, quantities):

            if not product_id or not qty:
                continue

            product = Product.objects.get(id=product_id)
            qty = int(qty)

            if product.quantity < qty:
                messages.error(request, f"{product.name} is out of stock!")
                return redirect('add_order')

        # =========================
        # ✅ STEP 2: CREATE ORDER SAFELY
        # =========================
        try:
            with transaction.atomic():

                order = Order.objects.create(customer=customer)

                for product_id, qty in zip(product_ids, quantities):

                    if not product_id or not qty:
                        continue

                    product = Product.objects.get(id=product_id)
                    qty = int(qty)

                    # CREATE ITEM
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=qty
                    )

                    # REDUCE STOCK
                    product.quantity -= qty
                    product.save()

                # SEND EMAIL
                send_invoice_email(order)

                messages.success(request, "Order created successfully!")
                return redirect('order_list')

        except Exception as e:
            messages.error(request, "Something went wrong!")
            return redirect('add_order')

    return render(request, 'orders/add_order.html', {
        'customers': customers,
        'products': products,
        'products_json': products_json
    })


def delete_order(request, id):
    order = get_object_or_404(Order, id=id)

    # ✅ RESTORE STOCK FOR ALL ITEMS
    for item in order.items.all():
        product = item.product
        product.quantity += item.quantity
        product.save()

    # ✅ DELETE ORDER
    order.delete()

    messages.success(request, "Order deleted and stock restored!")
    return redirect('order_list')