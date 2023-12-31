# Generated by Django 4.1.7 on 2023-09-29 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('SALES_ORDER_ID', models.AutoField(primary_key=True, serialize=False)),
                ('ORDERDATE', models.DateField(blank=True, null=True)),
                ('AMOUNT', models.IntegerField(blank=True, default=0, null=True)),
                ('STATUS', models.CharField(blank=True, max_length=35, null=True)),
                ('CUSTOMER_ID', models.ForeignKey(db_column='CUSTOMER_ID', on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
    ]
