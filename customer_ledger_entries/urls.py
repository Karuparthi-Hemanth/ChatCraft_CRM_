from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('add/', views.addCustomerLedgerEntry),
    path('get/',views.getCustomerLedgerEntry),
    path('edit/<int:customer_ledger_entry_id>/',views.editCustomerLedgerEntry),
    path('delete/<int:customer_ledger_entry_id>/',views.deleteCustomerLedgerEntry)
]