
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest,HttpResponse
from .models import CustomerLedgerEntry
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from .forms import CustomerLedgerEntryForm
from django.db.models import Max

# Create your views here.
def getCustomerLedgerEntry(request : HttpRequest):
    data = request.GET
    CustomerLedgerEntry = CustomerLedgerEntry.objects.all()

    filter_fields =["CUSTOMER_LEDGER_ENTRY_ID", "CUSTOMER_ID", "SALES_INVOICE_ID", "AMOUNT", "PAID_DATE"]
    
    for field in filter_fields:
        param_value = data.get(field)
        if param_value:
            CustomerLedgerEntry = CustomerLedgerEntry.filter(**{field: param_value})
            
    CustomerLedgerEntry_list = []

    for customerledger in CustomerLedgerEntry:
        customer_ledger_details = {
            "CUSTOMER_LEDGER_ENTRY_ID":customerledger.CUSTOMER_LEDGER_ENTRY_ID,
            "CUSTOMER_ID": customerledger.CUSTOMER_ID,
            "SALES_INVOICE_ID": customerledger.SALES_INVOICE_ID,
            "AMOUNT": customerledger.AMOUNT,
            "PAID_DATE": customerledger.PAID_DATE,
        }
        CustomerLedgerEntry_list.append(customer_ledger_details)

    ledger_data = json.dumps(CustomerLedgerEntry_list, indent=4)
    print(ledger_data)
    return HttpResponse(ledger_data, content_type="text/plain")
    # return render(request, 'Customers/display_customers.html', {'customers':customers})

@csrf_exempt
def addCustomerLedgerEntry(request : HttpRequest):
    data=request.POST.copy()
    form = CustomerLedgerEntryForm(data)
    if form.is_valid():
        form.save()
        return HttpResponse("added")
    else:
        error_json = form.errors.as_json()
        return HttpResponse(error_json, content_type='application/json')


@csrf_exempt
def editCustomerLedgerEntry(request, customer_ledger_entry_id):
    instance = get_object_or_404(CustomerLedgerEntry, CUSTOMER_LEDGER_ENTRY_ID=customer_ledger_entry_id)
    if request.method == 'POST':
        form = CustomerLedgerEntryForm(request.POST, instance=instance)
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
        form = CustomerLedgerEntryForm(instance=instance)
    return HttpResponse("updated")
    # return render(request, 'Customer/edit_Customer.html', {'form': form, 'instance': instance})

@csrf_exempt
def deleteCustomerLedgerEntry(request,customer_ledger_entry_id):
    sop = CustomerLedgerEntry.objects.filter(CUSTOMER_LEDGER_ENTRY_ID=customer_ledger_entry_id)
    sop.delete()
    return HttpResponse("deleted")

    # return redirect('/customers/get/')