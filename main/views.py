from django.shortcuts import render

from .models import *


# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def guests(request):
    return render(request, 'main/guests.html')


def overview(request):
    return render(request, 'main/overview.html')


def checklist(request):
    # data = {
    #     'title': 'Online Wedding Planner | Список дел'
    # }
    taskGroupList = TaskGroup.objects.all()
    tasks = Task.objects.all()

    # def assign_tasks_to_groups():
    for group in taskGroupList:
        group.tasks = list(filter(lambda task: task.task_group_id == group, tasks))


    return render(request, 'main/checklist.html', {'taskGroupList': taskGroupList})

# assign_tasks_to_groups()


# def add_tasks(request):
#     print(request.POST['task-group-name'])
#     return HttpResponseRedirect("checklist")
