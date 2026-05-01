from django.urls import path
from . import views

urlpatterns = [

    path('', views.order_list, name='order_list'),

    path('add/', views.add_order, name='add_order'),

    path('delete/<int:id>/', views.delete_order, name='delete_order'),

    path('invoice/<int:id>/', views.invoice_view, name='invoice'),

    path('invoice/pdf/<int:id>/', views.invoice_pdf, name='invoice_pdf'),

]