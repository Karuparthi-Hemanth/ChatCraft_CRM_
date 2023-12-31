
from django.db import models
from customers.models import Customer
from sales_orders.models import SalesOrder 
# Create your models here.
from django.db import models
from datetime import datetime
class SalesInvoice(models.Model):
    SALES_INVOICE_ID = models.AutoField(primary_key=True)
    SALES_ORDER_ID = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, db_column="SALES_ORDER_ID")
    CUSTOMER_ID = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column="CUSTOMER_ID", null=True, blank=True)
    TOTAL_AMOUNT = models.IntegerField(null=True, blank=True)
    TOTAL_ITEMS = models.IntegerField(null=True, blank=True)
    INVOICE_DATE = models.DateField(null=True, blank=True,default=datetime.now().date())
    STATUS = models.CharField(max_length=35, null=True, blank=True)

    def __str__(self):
        return f"{self.SALES_INVOICE_ID}"

    def save(self, *args, **kwargs):
        # Fetch the customer_id from the related SalesOrder and set it in CUSTOMER_ID
        if not self.CUSTOMER_ID:
            self.CUSTOMER_ID = self.SALES_ORDER_ID.CUSTOMER_ID
        super().save(*args, **kwargs)
