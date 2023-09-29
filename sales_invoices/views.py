from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,get_object_or_404
from .models import SalesInvoice
from .forms import SalesInvoiceForm
from sales_orders.models import SalesOrder
from sales_order_products.models import SalesOrderProduct
from django.http import HttpRequest,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

@csrf_exempt
def addSalesInvoice(request):
    data=request.POST.copy()
    form = SalesInvoiceForm(data)
    if form.is_valid():
        data["TOTAL_ITEMS"] = SalesOrderProduct.objects.filter(SALES_ORDER_ID = data["SALES_ORDER_ID"]).values("PRODUCT_ID").distinct().count()
        so = SalesOrder.objects.get(SALES_ORDER_ID = data["SALES_ORDER_ID"])
        data["TOTAL_AMOUNT"] = so.AMOUNT
        form = SalesInvoiceForm(data)
        if form.is_valid():
            form.save()
            return HttpResponse("added")
        else:
            error_json = form.errors.as_json()
            return HttpResponse(error_json, content_type='application/json')
    else:
        error_json = form.errors.as_json()
        return HttpResponse(error_json, content_type='application/json')
    








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
            "CUSTOMER_ID": sales_invoice.CUSTOMER_ID.CUSTOMER_ID,
            "INVOICE_DATE": sales_invoice.INVOICE_DATE,
            "STATUS" : sales_invoice.STATUS,
        }
        sales_invoice_list.append(sales_invoice_details)

    sales_invoice_data = json.dumps(sales_invoice_list, indent=4)
    return HttpResponse(sales_invoice_data)

    
@csrf_exempt
def editSalesInvoice(request, sales_invoice_id):
    instance = get_object_or_404(SalesInvoice, pk=sales_invoice_id)
    if request.method == 'POST':
        form = SalesInvoiceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # Redirect to a success page or show a success message
            return HttpResponse("saved")
        else:
            error_json = form.errors.as_json()
            return HttpResponse(error_json, content_type='application/json')

@csrf_exempt
def deleteSalesInvoice(request, sales_invoice_id):
    sale_invoice = get_object_or_404(SalesInvoice, pk=sales_invoice_id)
    sale_invoice.delete()
    return HttpResponse('deleted')