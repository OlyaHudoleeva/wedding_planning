from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def guests(request):
    return render(request, 'main/guests.html')


def overview(request):
    return render(request, 'main/overview.html')


def checklist(request):
    data = {
        'title': 'Online Wedding Planner | Список дел'
    }
    return render(request, 'main/checklist.html', data)


def add_tasks(request):
    print(request.POST['task-group-name'])
    return HttpResponseRedirect("checklist")
