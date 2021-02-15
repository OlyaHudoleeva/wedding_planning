from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("<h4>Main page</h4>")

def guests(request):
    return HttpResponse("<h4>Guests list</h4>")
