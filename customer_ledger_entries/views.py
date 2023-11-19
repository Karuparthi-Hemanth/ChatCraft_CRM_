
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
from customers.models import Customer
from sales_invoices.models import SalesInvoice
# Create your views here.
def getCustomerLedgerEntry(request : HttpRequest):
    data = request.GET
    CustomerLedgerEntries = CustomerLedgerEntry.objects.all()

    filter_fields =["CUSTOMER_LEDGER_ENTRY_ID", "CUSTOMER_ID", "SALES_INVOICE_ID", "AMOUNT", "PAID_DATE"]
    
    for field in filter_fields:
        param_value = data.get(field)
        if param_value:
            CustomerLedgerEntries = CustomerLedgerEntries.filter(**{field: param_value})
            
        print(CustomerLedgerEntries)
    CustomerLedgerEntrieslist = []

    for customerledger in CustomerLedgerEntries:
        customer_ledger_details = {
            "CUSTOMER_LEDGER_ENTRY_ID":customerledger.CUSTOMER_LEDGER_ENTRY_ID,
            "CUSTOMER_ID": str(customerledger.CUSTOMER_ID),
            "SALES_INVOICE_ID": str(customerledger.SALES_INVOICE_ID),
            "AMOUNT": customerledger.AMOUNT,
            "PAID_DATE": str(customerledger.PAID_DATE),
        }
        CustomerLedgerEntrieslist.append(customer_ledger_details)

    ledger_data = json.dumps(CustomerLedgerEntrieslist, indent=4)
    # return HttpResponse(ledger_data, content_type="text/plain")
    return render(request, 'CustomerLedgerEntry/display_customer_ledger_entries.html', 
                  {'CustomerLedgerEntries':CustomerLedgerEntries,'form':CustomerLedgerEntryForm()})

@csrf_exempt
def addCustomerLedgerEntry(request : HttpRequest):
    if request.method == 'POST':
        data=request.POST.copy()
        form = CustomerLedgerEntryForm(data)
        if form.is_valid():
            updatecustomerbalance(data['CUSTOMER_ID'],data['AMOUNT'])
            updatesalesinvoice(data)
            form.save()
            # return HttpResponse("added")
            return redirect('/customer_ledger_entries/get/')
        # else:
        #     error_json = form.errors.as_json()
        #     return HttpResponse(error_json, content_type='application/json')
    else:
        form = CustomerLedgerEntryForm()
    return render(request, 'CustomerLedgerEntry/save_customer_ledger_entry.html', {'form':form})    

@csrf_exempt
def editCustomerLedgerEntry(request, customer_ledger_entry_id):
    instance = get_object_or_404(CustomerLedgerEntry, CUSTOMER_LEDGER_ENTRY_ID=customer_ledger_entry_id)
    if request.method == 'POST':
        form = CustomerLedgerEntryForm(request.POST, instance=instance)
        print(form.errors)
        if form.is_valid():
            # print("Form Data:", form.cleaned_data)
            form.save()
            # Redirect to a success page or show a success message
            # return HttpResponse("Sales Order Product created successfully")
            return redirect('/customer_ledger_entries/get/')
        # else:
        #     error_json = form.errors.as_json()
        #     return HttpResponse(error_json, content_type='application/json')
    else:
        form = CustomerLedgerEntryForm(instance=instance)
    # return HttpResponse("updated")
    return render(request, 'CustomerLedgerEntry/save_customer_ledger_entry.html', {'form': form, 'instance': instance})

@csrf_exempt
def deleteCustomerLedgerEntry(request,customer_ledger_entry_id):
    sop = CustomerLedgerEntry.objects.filter(CUSTOMER_LEDGER_ENTRY_ID=customer_ledger_entry_id)
    sop.delete()
    # return HttpResponse("deleted")
    return redirect('/customer_ledger_entries/get/')

@csrf_exempt
def updatecustomerbalance(customer_id,amount):
    customer=Customer.objects.get(CUSTOMER_ID=customer_id)
    customer.BALANCE_DUE=int(customer.BALANCE_DUE)-int(amount)
    customer.save()

def updatesalesinvoice(data):
    sale_invoice=SalesInvoice.objects.get(SALES_INVOICE_ID=data['SALES_INVOICE_ID'])
    customer_ledger_entries=CustomerLedgerEntry.objects.filter(CUSTOMER_ID=data['CUSTOMER_ID'],
                                                               SALES_INVOICE_ID=data['SALES_INVOICE_ID'])
    sum=0
    for entry in customer_ledger_entries:
        sum+=int(entry.AMOUNT)
    if(sum>=int(sale_invoice.TOTAL_AMOUNT)):
        sale_invoice.STATUS='paid'
        sale_invoice.save()