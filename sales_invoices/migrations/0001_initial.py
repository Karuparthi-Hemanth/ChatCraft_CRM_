# Generated by Django 4.1.7 on 2023-09-29 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('sales_orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesInvoice',
            fields=[
                ('SALESINVOICE_ID', models.AutoField(primary_key=True, serialize=False)),
                ('TOTAL_AMOUNT', models.IntegerField(blank=True, null=True)),
                ('TOTAL_ITEMS', models.IntegerField(blank=True, null=True)),
                ('INVOICE_DATE', models.DateField(blank=True, null=True)),
                ('STATUS', models.CharField(blank=True, max_length=35, null=True)),
                ('CUSTOMER_ID', models.ForeignKey(db_column='CUSTOMER_ID', on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('SALES_ORDER_ID', models.ForeignKey(db_column='SALES_ORDER_ID', on_delete=django.db.models.deletion.CASCADE, to='sales_orders.salesorder')),
            ],
        ),
    ]
