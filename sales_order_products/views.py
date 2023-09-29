from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest,HttpResponse
from .models import SalesOrderProduct
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from .forms import SalesOrderProductForm
from django.db.models import Max

# Create your views here.
def getSalesOrderProduct(request : HttpRequest):
    data = request.GET
    SalesOrderProduct = SalesOrderProduct.objects.all()

    filter_fields =["SALES_ORDER_ID", "SEQ_NUM", "PRODUCT_ID", "AMOUNT", "QUANTITY"]
    
    for field in filter_fields:
        param_value = data.get(field)
        if param_value:
            SalesOrderProduct = SalesOrderProduct.filter(**{field: param_value})
            
    SalesOrderProduct_list = []

    for orderproduct in SalesOrderProduct:
        order_product_details = {
            "SALES_ORDER_ID":SalesOrderProduct.SALES_ORDER_ID,
            "SEQ_NUM": SalesOrderProduct.SEQ_NUM,
            "PRODUCT_ID": SalesOrderProduct.PRODUCT_ID,
            "AMOUNT": SalesOrderProduct.AMOUNT,
            "QUANTITY": SalesOrderProduct.QUANTITY,
        }
        SalesOrderProduct_list.append(customer_details)

    OrderProduct_data = json.dumps(SalesOrderProduct_list, indent=4)
    print(OrderProduct_data)
    return HttpResponse(OrderProduct_data, content_type="text/plain")
    # return render(request, 'Customers/display_customers.html', {'customers':customers})

@csrf_exempt
def addSalesorderProduct(request : HttpRequest):
    data=request.POST.copy()
    max_seq_num = SalesOrderProduct.objects.filter(SALES_ORDER_ID=data["SALES_ORDER_ID"]).aggregate(Max('SEQ_NUM'))['SEQ_NUM__max']
    if max_seq_num is None:
        max_seq_num=0
    print(max_seq_num)
    data["SEQ_NUM"]=max_seq_num+1
    form = SalesOrderProductForm(data)
    if form.is_valid():
        form.save()
        return HttpResponse("added")
    else:
        error_json = form.errors.as_json()
        return HttpResponse(error_json, content_type='application/json')


@csrf_exempt
def editSalesOrderProduct(request, sales_order_id,seq_num):
    instance = get_object_or_404(SalesOrderProduct, pk=(Sales_Order_id,Seq_Num))

    if request.method == 'POST':
        form = SalesOrderProductForm(request.POST, instance=instance)
        print(form.errors)
        if form.is_valid():
            print("Form Data:", form.cleaned_data)
            form.save()
            # Redirect to a success page or show a success message
            return HttpResponse("Sales Order Product created successfully")
        else:
            error_json = form.errors.as_json()
            return HttpResponse(error_json, content_type='application/json')
    else:
        form = SalesOrderProductForm(instance=instance)
    return HttpResponse("updated")
    # return render(request, 'Customer/edit_Customer.html', {'form': form, 'instance': instance})

@csrf_exempt
def deleteSalesOrderProduct(request,sales_order_id):
    sop = SalesOrderProduct.objects.filter(SALES_ORDER_ID=sales_order_id)
    sop.delete()
    return HttpResponse("deleted")

    # return redirect('/customers/get/')