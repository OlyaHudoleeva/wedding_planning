from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def guests(request):
    return render(request, 'main/guests.html')

def overview(request):
    return render(request, 'main/overview.html')
