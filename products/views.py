from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest,HttpResponse
from .models import Product
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
# Create your views here.
@csrf_exempt
def addProduct(request : HttpRequest):
    data = request.POST
    p=Product(PRODUCT_NAME = data["PRODUCT_NAME"],
              UOM = data["UOM"],
              QUANTITY_ON_HAND = data["QUANTITY_ON_HAND"],
              COST = data["COST"],
              STATUS = data["STATUS"])
    p.save()
    return HttpResponse("created")

@csrf_exempt
def editProduct(request,product_id:int):
    data = request.POST
    p = Product.objects.get(PRODUCT_ID = product_id)
    p.PRODUCT_NAME = data["PRODUCT_NAME"]
    p.QUANTITY_ON_HAND = data["QUANTITY_ON_HAND"]
    p.COST = data["COST"]
    p.STATUS = data["STATUS"]
    p.UOM = data["UOM"]
    p.save()
    return HttpResponse("updated")


@csrf_exempt
def deleteProduct(request,product_id:int):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return HttpResponse("deleted")

@csrf_exempt
def getProduct(request: HttpRequest):
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

    return HttpResponse(product_data, content_type="application/json")