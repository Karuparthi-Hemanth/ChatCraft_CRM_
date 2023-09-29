from django.urls import path
from . import views
urlpatterns = [
    path('add/', views.addCustomer),
    path('get/', views.getCustomer),
    path('edit/<int:customer_id>/',views.editCustomer),
    path('delete/<int:customer_id>/',views.deleteCustomer),
]