# Generated by Django 4.1.7 on 2023-09-29 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales_invoices', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesinvoice',
            old_name='SALESINVOICE_ID',
            new_name='SALES_INVOICE_ID',
        ),
    ]
