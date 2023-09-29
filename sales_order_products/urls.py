from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('add/', views.addSalesorderProduct),
    path('get/',views.getSalesOrderProduct),
    path('edit/<int:sales_order_id>/<int:seq_num>/',views.editSalesOrderProduct),
    path('delete/<int:sales_order_id>/',views.deleteSalesOrderProduct)
]