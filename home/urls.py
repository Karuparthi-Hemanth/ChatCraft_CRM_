from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MyHomePage),
    path('perform/', views.perform),
    path('getcolumns/',views.getColumnsByModule),
]