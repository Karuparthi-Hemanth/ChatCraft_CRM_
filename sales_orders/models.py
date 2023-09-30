from django.db import models
import datetime
from customers.models import Customer

class SalesOrder(models.Model):
    SALES_ORDER_ID=models.AutoField(primary_key=True)
    CUSTOMER_ID=models.ForeignKey(Customer,on_delete=models.CASCADE,db_column="CUSTOMER_ID")
    ORDERDATE = models.DateField(blank=True, null=True)
    AMOUNT=models.IntegerField(default =0 ,null=True,blank = True)
    STATUS = models.CharField(max_length=35,null=True,blank = True)

    def __str__(self):
        return f"{self.SALES_ORDER_ID}"