# Generated by Django 4.2.4 on 2023-09-29 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('sales_invoices', '0002_rename_salesinvoice_id_salesinvoice_sales_invoice_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerLedgerEntry',
            fields=[
                ('CUSTOMER_LEDGER_ENTRY_ID', models.AutoField(primary_key=True, serialize=False)),
                ('AMOUNT', models.IntegerField(null=True)),
                ('PAID_DATE', models.DateField()),
                ('CUSTOMER_ID', models.ForeignKey(db_column='CUSTOMER_ID', on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('SALES_INVOICE_ID', models.ForeignKey(db_column='SALES_INVOICE_ID', on_delete=django.db.models.deletion.CASCADE, to='sales_invoices.salesinvoice')),
            ],
        ),
    ]
