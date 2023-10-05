from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('add/<int:sales_order_id>/', views.addSalesorderProduct),
    path('get/<int:sales_order_id>/',views.getSalesOrderProduct),
    path('edit/<int:sales_order_id>/<int:seq_num>/',views.editSalesOrderProduct),
    path('delete/<int:sales_order_id>/<int:seq_num>/',views.deleteSalesOrderProduct)
]