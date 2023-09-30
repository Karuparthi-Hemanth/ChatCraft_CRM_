from django.shortcuts import render
from django.http import HttpRequest

def MyHomePage(request: HttpRequest):
    return render(request, 'home/dashboard.html')