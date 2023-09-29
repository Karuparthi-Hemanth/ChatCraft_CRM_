from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('add/', views.addSalesInvoice),
    path('get/', views.getSalesInvoice),
    path('edit/<int:sales_invoice_id>/',views.editSalesInvoice),
    path('delete/<int:sales_invoice_id>/',views.deleteSalesInvoice)
]