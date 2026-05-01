from django.shortcuts import render
from orders.models import Order, OrderItem
from customers.models import Customer
from products.models import Product
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):

    # =========================
    # COUNTS
    # =========================
    total_orders = Order.objects.count()
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()

    # =========================
    # TOTAL REVENUE
    # =========================
    total_revenue = OrderItem.objects.aggregate(
        total=Sum(F('product__price') * F('quantity'))
    )['total'] or 0

    # =========================
    # LOW STOCK
    # =========================
    low_stock_products = Product.objects.filter(quantity__lt=5)

    # =========================
    # RECENT ORDERS
    # =========================
    recent_orders = Order.objects.all().order_by('-id')[:5]

    # =========================
    # MONTHLY REVENUE
    # =========================
    monthly_data = (
        OrderItem.objects
        .annotate(month=TruncMonth('order__created_at'))
        .values('month')
        .annotate(total=Sum(F('product__price') * F('quantity')))
        .order_by('month')
    )

    months = [data['month'].strftime("%b") for data in monthly_data if data['month']]
    revenues = [float(data['total']) for data in monthly_data if data['total']]

    # =========================
    # PRODUCT PIE DATA
    # =========================
    product_data = (
        OrderItem.objects
        .values('product__name')
        .annotate(total=Sum(F('product__price') * F('quantity')))
        .order_by('-total')
    )

    product_names = [item['product__name'] for item in product_data]
    product_totals = [float(item['total']) for item in product_data]

    # ✅ FINAL CONTEXT (ALL IN ONE)
    context = {
        'total_orders': total_orders,
        'total_customers': total_customers,
        'total_products': total_products,
        'total_revenue': total_revenue,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'months': months,
        'revenues': revenues,
        'product_names': product_names,
        'product_totals': product_totals,
    }

    return render(request, 'dashboard/dashboard.html', context)