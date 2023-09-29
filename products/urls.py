from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('add/', views.addProduct),
    path('get/', views.getProduct),
    path('edit/<int:product_id>/',views.editProduct),
    path('delete/<int:product_id>/',views.deleteProduct)
]
