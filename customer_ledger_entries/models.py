from django.db import models
from customers.models import Customer
from sales_invoices.models import SalesInvoice
# Create your models here.
class CustomerLedgerEntry(models.Model):
    CUSTOMER_LEDGER_ENTRY_ID=models.AutoField(primary_key=True)
    CUSTOMER_ID=models.ForeignKey(Customer,on_delete=models.CASCADE,db_column="CUSTOMER_ID")
    SALES_INVOICE_ID = models.ForeignKey(SalesInvoice,on_delete=models.CASCADE,db_column="SALES_INVOICE_ID")
    AMOUNT=models.IntegerField(null=True)
    PAID_DATE = models.DateField(null=True,blank=True)