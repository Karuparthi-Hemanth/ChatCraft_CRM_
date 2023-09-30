from django.db import models

# Create your models here.
class Product(models.Model):
    PRODUCT_ID=models.AutoField(primary_key=True)
    PRODUCT_NAME = models.CharField(max_length=35,unique = True)
    UOM=models.CharField(max_length=35,null=True,blank=True)
    COST = models.IntegerField(default=0,null=True,blank=True)
    QUANTITY_ON_HAND=models.IntegerField(default = 0,null=True,blank=True)
    STATUS = models.CharField(max_length=35,null = True,blank=True)
    
    def __str__(self):
        return f"{self.PRODUCT_ID} -- {self.PRODUCT_NAME}"
