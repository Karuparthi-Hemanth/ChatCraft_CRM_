# Create your models here.
from django.db import models

# Create your models here.
class Customer(models.Model):
    CUSTOMER_ID=models.AutoField(primary_key=True)
    COMPANY_NAME=models.CharField(max_length=35,unique=True)
    BALANCE_DUE=models.IntegerField(default=0,blank=True,null=True)
    ADDRESS = models.CharField(max_length=35,null=True,blank=True)
    STATUS = models.CharField(max_length=35,null=True,blank=True)
    CONTACT = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return f"{self.CUSTOMER_ID} -- {self.COMPANY_NAME}"
