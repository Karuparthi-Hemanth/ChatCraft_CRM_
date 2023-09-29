from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest,HttpResponse
from .models import Product
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from .forms import ProductForm

# Create your views here.
def getProduct(request : HttpRequest):
    data = request.GET
    products = Product.objects.all()

    filter_fields = ["PRODUCT_NAME", "UOM", "QUANTITY_ON_HAND", "STATUS", "COST"]
    
    for field in filter_fields:
        param_value = data.get(field)
        if param_value:
            products = products.filter(**{field: param_value})

    # Create a list to store product details as dictionaries
    product_list = []

    # Extract and format product details
    for product in products:
        product_details = {
            'PRODUCT_ID': product.PRODUCT_ID,
            'PRODUCT_NAME': product.PRODUCT_NAME,
            'UOM': product.UOM,
            'COST': product.COST,
            'QUANTITY_ON_HAND': product.QUANTITY_ON_HAND,
            'STATUS': product.STATUS,
        }
        product_list.append(product_details)

    # Convert the product_list to JSON
    product_data = json.dumps(product_list, indent=4)
    return HttpResponse(product_data)

@csrf_exempt
def addProduct(request : HttpRequest):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("added")
    else:
        error_json = form.errors.as_json()
        return HttpResponse(error_json, content_type='application/json')

@csrf_exempt
def editProduct(request, product_id):
    instance = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # Redirect to a success page or show a success message
            return HttpResponse("edited") 
    else:
        error_json = form.errors.as_json()
        return HttpResponse(error_json, content_type='application/json')

@csrf_exempt
def deleteProduct(request, product_id):
    data = request.POST
    product = get_object_or_404(Product, pk=product_id)
    product.delete()

    return redirect('/products/get/')