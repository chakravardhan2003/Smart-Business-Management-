from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ AUTH
    path('auth/', include('authentication.urls')),

    # ✅ MAIN APPS
    path('dashboard/', include('dashboard.urls')),
    path('orders/', include('orders.urls')),
    path('products/', include('products.urls')),
    path('customers/', include('customers.urls')),
]