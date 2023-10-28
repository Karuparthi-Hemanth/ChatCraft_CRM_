from django.shortcuts import render,redirect
from django.http import HttpRequest
import requests

def MyHomePage(request: HttpRequest):
    if request.user.is_authenticated:
        return render(request, 'home/dashboard.html')
    else:
        return redirect('/users/login/')

from django.shortcuts import render    
import json
from django.apps import apps
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
dict={                                
   'products' : 'Product',
   'customers' : 'Customer',
   'sales_orders' : 'SalesOrder',
   'sales_order_products' : 'SalesOrderProduct',
   'sales_invoices' : 'SalesInvoice'
}
@csrf_exempt
def getColumnsByModule(request):
    print(request)
    data = json.loads(request.body.decode('utf-8'))
    module_name = data.get("module")
    action = data.get("action")
    model_class = apps.get_model(app_label=module_name, model_name=dict[module_name])
    model_fields = model_class._meta.get_fields()
    fields = [field.name for field in model_fields if not field.is_relation and not field.primary_key]
    return HttpResponse(json.dumps(fields))

@csrf_exempt
def perform(request):
    data = json.loads(request.body.decode('utf-8'))
    module = data.get("module")
    action = data.get("action")
    filter_data = data.get("filter", {}) # Directly access filter as a dictionary
    new_data = data.get("new_data", {})  # Directly access new_data as a dictionary
    keys_to_delete = []
    for key in filter_data.keys():
        if(filter_data[key]==' '):
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del filter_data[key]
    keys_to_delete=[]
    for key in new_data.keys():
        if(new_data[key]==' '):
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del new_data[key]
    # print(module)
    model = apps.get_model(app_label=module, model_name=dict[module])
    queryset = model.objects.all()
    for field, value in filter_data.items():
      # Filter the queryset based on filter_data
        filter_kwargs = {field: value}
        queryset = queryset.filter(**filter_kwargs)

    url='http://localhost:8000/'+module+'/'+str(action)+'/'

    if action == 'delete':
        for row in queryset:
            model_class = apps.get_model(app_label=module, model_name=dict[module])
            print("before")
            pk_fields = getPkFieldsInfo(row,model_class._meta.fields)
            print(pk_fields)
            print("after")
            url_copy = url
            for pk_field in pk_fields:
                url_copy+=str(pk_field)
                url_copy+='/'
            print(url_copy)
            requests.post(url_copy)
        return HttpResponse("Records deleted successfully")
    
    if action == 'edit':
        for row in queryset:
            # Get column names for the module
            model_class = apps.get_model(app_label=module, model_name=dict[module])
            print("before")
            pk_fields = getPkFieldsInfo(row,model_class._meta.fields)
            print(pk_fields)
            print("after")
            url_copy = url
            for pk_field in pk_fields:
                url_copy+=str(pk_field)
                url_copy+='/'
            print(url_copy)
            requests.post(url_copy,new_data)
            row.save()
        return HttpResponse("Records edited successfully")

    if action == 'add':
        requests.post(url,new_data)
        return HttpResponse("Records inserted successfully")

    return HttpResponse("Invalid action", status=200)

def getPkFieldsInfo(row,model):
    pk_field = []
    print(row)
    print(model)
    unique_field = []
    for field in model:
        if field.primary_key:
            pk_field.append(getattr(row, field.name))
            break
    if len(pk_field) == 0:
        for field in model:
            if field.unique:
                unique_field.append(getattr(row, field.name))
        return unique_field
    return pk_field