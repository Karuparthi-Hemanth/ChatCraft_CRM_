from django.shortcuts import render
from django.apps import apps
from django.http import HttpResponse
import json
# Create your views here.
dict={
   'products' : 'Product',
   'customers' : 'Customer'
}
def getColumnsByModule(request):
   module_name = request.GET['module_name']
   model_class = apps.get_model(module_name,dict[module_name])
   model_fields = model_class._meta.get_fields()
   fields = [field.name for field in model_fields]
   result=json.dumps(fields)
   return HttpResponse(result)


