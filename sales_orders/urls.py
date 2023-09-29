from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('add/', views.addSalesOrder),
    path('get/', views.getSalesOrder),
    path('edit/<int:sales_order_id>/',views.editSalesOrder),
    path('delete/<int:sales_order_id>/',views.deleteSalesOrder)
]