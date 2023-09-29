from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest,HttpResponse
from .models import Customer
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from .forms import CustomerForm

# Create your views here.
def getCustomer(request : HttpRequest):
    data = request.GET
    customers = Customer.objects.all()

    filter_fields =["COMPANY_NAME", "BALANCE_DUE", "ADDRESS", "STATUS", "CONTACT"]
    
    for field in filter_fields:
        param_value = data.get(field)
        if param_value:
            customers = customers.filter(**{field: param_value})
            
    customer_list = []

    for customer in customers:
        customer_details = {
            "CUSTOMER_ID":customer.CUSTOMER_ID,
            "COMPANY_NAME": customer.COMPANY_NAME,
            "BALANCE_DUE": customer.BALANCE_DUE,
            "ADDRESS": customer.ADDRESS,
            "STATUS": customer.STATUS,
            "CONTACT" : customer.CONTACT,
        }
        customer_list.append(customer_details)

    customer_data = json.dumps(customer_list, indent=4)
    return HttpResponse(customer_data)

@csrf_exempt
def addCustomer(request : HttpRequest):
    form = CustomerForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("added")
    else:
        error_json = form.errors.as_json()
        return HttpResponse(error_json, content_type='application/json')
    
@csrf_exempt
def editCustomer(request, customer_id):
    instance = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # Redirect to a success page or show a success message
            return HttpResponse("saved")
        else:
            error_json = form.errors.as_json()
            return HttpResponse(error_json, content_type='application/json')

@csrf_exempt
def deleteCustomer(request, customer_id):
    data = request.POST
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.delete()
    return redirect('/customers/get/')