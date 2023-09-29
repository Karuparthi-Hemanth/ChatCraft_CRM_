
# Create your models here.
from django.db import models
from products.models import Product
from sales_orders.models import SalesOrder

class SalesOrderProduct(models.Model):
    SALES_ORDER_ID = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE,
        db_column="SALES_ORDER_ID"
    )
    SEQ_NUM = models.IntegerField(default=0)
    PRODUCT_ID = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column="PRODUCT_ID"
    )
    QUANTITY = models.IntegerField(null=True, blank=True)
    AMOUNT = models.IntegerField(null=True, blank=True)

    class Meta:
        models.UniqueConstraint(fields=['SALES_ORDER_ID', 'SEQ_NUM'], name="article_editor_id",)