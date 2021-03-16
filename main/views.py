from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def guests(request):
    bride_side_guests = Guest.objects.filter(side="B")
    groom_side_guests = Guest.objects.filter(side="G")

    return render(request, 'main/guests.html',
                  {'bride_side_guests': bride_side_guests, 'groom_side_guests': groom_side_guests})


def overview(request):
    return render(request, 'main/overview.html')

@login_required
def checklist(request):
    # data = {
    #     'title': 'Online Wedding Planner | Список дел'
    # }
    error = ''
    if request.method == "POST":
        taskGroupForm = TaskGroupForm(request.POST)
        taskGroupForm.instance.user = User.objects.get(id=1)
        if taskGroupForm.is_valid():
            taskGroupForm.save()
            return redirect('checklist')
        else:
            error = 'Данные введены некорректно'

    taskGroupList = TaskGroup.objects.filter(user=request.user)
    tasks = Task.objects.all()

    for group in taskGroupList:
        group.tasks = list(filter(lambda task: task.task_group == group, tasks))

    taskGroupForm = TaskGroupForm()

    return render(request, 'main/checklist.html',
                  {'taskGroupList': taskGroupList, 'taskGroupForm': taskGroupForm, 'error': error})

# def createTaskGroup(request):
#     taskGroupForm = TaskGroupForm()
#
#     data = {'taskGroupForm' : taskGroupForm}
#     response = checklist(request, data)
#     return response


# def add_tasks(request):
#     print(request.POST['task-group-name'])
#     return HttpResponseRedirect("checklist")
