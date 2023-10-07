from django.shortcuts import render,get_object_or_404, redirect
from .models import SalesInvoice
from .forms import SalesInvoiceForm
from sales_orders.models import SalesOrder
from sales_order_products.models import SalesOrderProduct
from django.http import HttpRequest,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sales_order_products.views import getSalesOrderProduct
import json
from django.core import serializers
from products.models import Product
from django.forms.models import model_to_dict
from customers.models import Customer
# Create your views here.

@csrf_exempt
def addSalesInvoice(request):
    if request.method == 'POST':
        data=request.POST.copy()
        form = SalesInvoiceForm(data)
        if form.is_valid():
            data["TOTAL_ITEMS"] = SalesOrderProduct.objects.filter(SALES_ORDER_ID = data["SALES_ORDER_ID"]).values("PRODUCT_ID").distinct().count()
            so = SalesOrder.objects.get(SALES_ORDER_ID = data["SALES_ORDER_ID"])
            data["TOTAL_AMOUNT"] = so.AMOUNT
            form = SalesInvoiceForm(data)
            if form.is_valid():
                deductProduct(request,data["SALES_ORDER_ID"])
                sales_invoice_instance = form.save()
                # Convert the instance data to a dictionary
                sales_invoice_data = model_to_dict(sales_invoice_instance)
                # Convert the dictionary to a JSON string
                sales_invoice_json = json.dumps(sales_invoice_data)
                updatecustomerbalance(sales_invoice_json)
                # return HttpResponse("added")
                return redirect('/sales_invoices/get/')
            else:
                error_json = form.errors.as_json()
                return HttpResponse(error_json, content_type='application/json')
        else:
            error_json = form.errors.as_json()
            return HttpResponse(error_json, content_type='application/json')
    else:
        form = SalesInvoiceForm()
        return render(request, 'SalesInvoice/save_sales_invoice.html', {'form':form})    

def getSalesInvoice(request : HttpRequest):
    data = request.GET
    sales_invoices = SalesInvoice.objects.all()

    filter_fields =["SALES_INVOICE_ID", "SALES_ORDER_ID", "CUSTOMER_ID", "INVOICE_DATE", "STATUS"]
    
    for field in filter_fields:
        param_value = data.get(field)
        if param_value:
            sales_invoices = sales_invoices.filter(**{field: param_value})
            
    sales_invoice_list = []

    for sales_invoice in sales_invoices:
        sales_invoice_details = {
            "SALES_INVOICE_ID":sales_invoice.SALES_INVOICE_ID,
            "SALES_ORDER_ID": sales_invoice.SALES_ORDER_ID.SALES_ORDER_ID,
            "CUSTOMER_ID": sales_invoice.CUSTOMER_ID_id,
            "INVOICE_DATE": str(sales_invoice.INVOICE_DATE),
            "STATUS" : sales_invoice.STATUS,
        }
        sales_invoice_list.append(sales_invoice_details)

    sales_invoice_data = json.dumps(sales_invoice_list, indent=4)
    # return HttpResponse(sales_invoice_data)
    return render(request, 'SalesInvoice/display_sales_invoice.html', {'sales_invoices':sales_invoices, 'form':SalesInvoiceForm()})
    
@csrf_exempt
def editSalesInvoice(request, sales_invoice_id):
    instance = get_object_or_404(SalesInvoice, pk=sales_invoice_id)
    if request.method == 'POST':
        form = SalesInvoiceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # Redirect to a success page or show a success message
            # return HttpResponse("saved")
            return redirect('/sales_invoices/get/') 
        else:
            error_json = form.errors.as_json()
            return HttpResponse(error_json, content_type='application/json')
    else:
        form = SalesInvoiceForm(instance=instance)
    return render(request, 'SalesInvoice/save_sales_invoice.html', {'form': form, 'instance': instance})

@csrf_exempt
def deleteSalesInvoice(request, sales_invoice_id):
    sale_invoice = get_object_or_404(SalesInvoice, pk=sales_invoice_id)
    sale_invoice.delete()
    # return HttpResponse('deleted')
    return redirect('/sales_invoices/get')

def deductProduct(request,sales_order_id):
    sales_order_products = SalesOrderProduct.objects.filter(SALES_ORDER_ID=sales_order_id)

    # Iterate through each sales_order_product object
    for sales_order_product in sales_order_products:
        product = sales_order_product.PRODUCT_ID 
        product_id = product.PRODUCT_ID
        prod = Product.objects.get(PRODUCT_ID=product_id)
        new_quantity=prod.QUANTITY_ON_HAND-sales_order_product.QUANTITY
        prod.QUANTITY_ON_HAND = new_quantity
        prod.save()
    #make status of sales_order billed
    sales_order=SalesOrder.objects.get(SALES_ORDER_ID=sales_order_id)
    sales_order.STATUS='invoiced'
    sales_order.save()

def updatecustomerbalance(data):
    data = json.loads(data)
    customer=Customer.objects.get(CUSTOMER_ID=int(data["CUSTOMER_ID"]))
    customer.BALANCE_DUE=customer.BALANCE_DUE+int(data["TOTAL_AMOUNT"])
    customer.save()
    return data