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
def getSalesOrderProduct(request : HttpRequest,sales_order_id):
    data = request.GET
    SalesOrderProduct1 = SalesOrderProduct.objects.filter(SALES_ORDER_ID=sales_order_id)

    filter_fields =["SALES_ORDER_ID", "SEQ_NUM", "PRODUCT_ID", "AMOUNT", "QUANTITY"]
    
    for field in filter_fields:
        param_value = data.get(field)
        if param_value:
            SalesOrderProduct1 = SalesOrderProduct1.filter(**{field: param_value})
            
    SalesOrderProduct_list = []

    for OrderProduct in SalesOrderProduct1:
        order_product_details = {
            "SALES_ORDER_ID":str(OrderProduct.SALES_ORDER_ID),
            "SEQ_NUM": OrderProduct.SEQ_NUM,
            "PRODUCT_ID": str(OrderProduct.PRODUCT_ID),
            "AMOUNT": OrderProduct.AMOUNT,
            "QUANTITY": OrderProduct.QUANTITY,
        }
        SalesOrderProduct_list.append(order_product_details)

    OrderProduct_data = json.dumps(SalesOrderProduct_list, indent=4)
    # return HttpResponse(OrderProduct_data, content_type="text/plain")
    return render(request, 'salesorderproducts/display_sop.html', {'sales_order_products':SalesOrderProduct_list, 'form':SalesOrderProductForm,'sales_order_id':sales_order_id})

@csrf_exempt
def addSalesorderProduct(request : HttpRequest,sales_order_id):
    if request.method == 'POST':
        data=request.POST.copy()
        max_seq_num = SalesOrderProduct.objects.filter(SALES_ORDER_ID=data["SALES_ORDER_ID"]).aggregate(Max('SEQ_NUM'))['SEQ_NUM__max']
        if max_seq_num is None:
            max_seq_num=0
        
        data["SALES_ORDER_ID"]=sales_order_id
        data["SEQ_NUM"]=max_seq_num+1
        form = SalesOrderProductForm(data)
        if form.is_valid():
            form.save()
            # return HttpResponse("added")
            return redirect('/sales_order_products/get/'+str(sales_order_id)+'/')
        else:
            error_json = form.errors.as_json()
            return HttpResponse(error_json, content_type='application/json')
    else:
        form = SalesOrderProductForm()
    return render(request, 'salesorderproducts/save_sop.html', {'form': form,'sales_order_id':sales_order_id})


@csrf_exempt
def editSalesOrderProduct(request, sales_order_id,seq_num):
    instance = get_object_or_404(SalesOrderProduct, SALES_ORDER_ID=sales_order_id, SEQ_NUM=seq_num)
    if request.method == 'POST':
        form = SalesOrderProductForm(request.POST, instance=instance)
        # print(form.errors)
        if form.is_valid():
            # print("Form Data:", form.cleaned_data)
            form.save()
            # Redirect to a success page or show a success message
            # return HttpResponse("Sales Order Product created successfully")
            return redirect('/sales_order_products/get/'+str(sales_order_id)+'/')
        else:
            error_json = form.errors.as_json()
            return HttpResponse(error_json, content_type='application/json')
    else:
        form = SalesOrderProductForm(instance=instance)
    # return HttpResponse("updated")
    return render(request, 'salesorderproducts/save_sop.html', {'form': form, 'instance': instance})

@csrf_exempt
def deleteSalesOrderProduct(request,sales_order_id,seq_num):
    sop = SalesOrderProduct.objects.filter(SALES_ORDER_ID=sales_order_id,SEQ_NUM=seq_num)
    sop.delete()
    # return HttpResponse("deleted")
    return redirect('/sales_order_products/get/'+str(sales_order_id)+'/')