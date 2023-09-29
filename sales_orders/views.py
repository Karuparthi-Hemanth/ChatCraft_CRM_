from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest,HttpResponse
from .models import SalesOrder
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from .forms import SalesOrderForm

# Create your views here.
def getSalesOrder(request : HttpRequest):
    data = request.GET
    sales_orders = SalesOrder.objects.all()

    filter_fields =["SALES_ORDER_ID", "CUSTOMER_ID", "ORDERDATE", "STATUS", "AMOUNT"]
    
    for field in filter_fields:
        param_value = data.get(field)
        if param_value:
            sales_orders = sales_orders.filter(**{field: param_value})
            
    sales_order_list = []

    for sales_order in sales_orders:
        sales_order_details = {
            "SALES_ORDER_ID":sales_order.SALES_ORDER_ID,
            "CUSTOMER_ID": sales_order.CUSTOMER_ID.CUSTOMER_ID,
            "ORDERDATE": sales_order.ORDERDATE,
            "STATUS": sales_order.STATUS,
            "AMOUNT" : sales_order.AMOUNT,
        }
        sales_order_list.append(sales_order_details)

    sales_order_data = json.dumps(sales_order_list, indent=4)
    return HttpResponse(sales_order_data)

@csrf_exempt
def addSalesOrder(request : HttpRequest):
    form = SalesOrderForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("added")
    else:
        error_json = form.errors.as_json()
        return HttpResponse(error_json, content_type='application/json')
    
@csrf_exempt
def editSalesOrder(request, sales_order_id):
    instance = get_object_or_404(SalesOrder, pk=sales_order_id)
    if request.method == 'POST':
        form = SalesOrderForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # Redirect to a success page or show a success message
            return HttpResponse("saved")
        else:
            error_json = form.errors.as_json()
            return HttpResponse(error_json, content_type='application/json')

@csrf_exempt
def deleteSalesOrder(request, sales_order_id):
    sale_order = get_object_or_404(SalesOrder, pk=sales_order_id)
    sale_order.delete()
    return HttpResponse('deleted')