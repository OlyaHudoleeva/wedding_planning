from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        register_form = CreateUserForm()
        if request.method == 'POST':
            register_form = CreateUserForm(request.POST)
            if register_form.is_valid():
                # user = register_form.save() #возможно выплюнет нового юзера, нужно проверить
                register_form.save()
                user = register_form.cleaned_data.get('username')
                messages.success(request, 'Аккаунт успешно создан для пользователя ' + user)

                return redirect('login')
            # TaskGroup(user=register).save()

    context = {'register_form': register_form}
    return render(request, 'main/registration.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Данные введены некорректно')
    context = {}
    return render(request, 'main/login_page.html', context)


def logout_user(request):
    logout(request, )
    return redirect('login')


def index(request):
    return render(request, 'main/index.html')


@login_required(login_url='login')
def guests(request):
    bride_side_guests = Guest.objects.filter(side="B")
    groom_side_guests = Guest.objects.filter(side="G")

    bride_side_amount = Guest.objects.filter(side="B").count()
    groom_side_amount = Guest.objects.filter(side="G").count()

    total_male = Guest.objects.filter(sex="M").count()
    total_female = Guest.objects.filter(sex="F").count()
    total_child = Guest.objects.filter(sex="C").count()

    return render(request, 'main/guests.html',
                  {'bride_side_guests': bride_side_guests, 'groom_side_guests': groom_side_guests,
                   'bride_side_amount': bride_side_amount, 'groom_side_amount': groom_side_amount,
                   'total_male': total_male, 'total_female': total_female, 'total_child': total_child})


@login_required(login_url='login')
def overview(request):
    return render(request, 'main/overview.html')


@login_required(login_url='login')
def checklist(request):
    # data = {
    #     'title': 'Online Wedding Planner | Список дел'
    # }
    error = ''
    if request.method == "POST":
        task_group_form = TaskGroupForm(request.POST)
        task_group_form.instance.user = User.objects.get(id=1)
        if task_group_form.is_valid():
            task_group_form.save()
            return redirect('checklist')
        else:
            error = 'Данные введены некорректно'

    if request.user.is_authenticated:
        task_group_list = TaskGroup.objects.filter(user=request.user)
    else:
        task_group_list = []
    tasks = Task.objects.all()

    for group in task_group_list:
        group.tasks = list(filter(lambda task: task.task_group == group, tasks))
        task_form = TaskForm()
        group.task_form = task_form

    task_group_form = TaskGroupForm()

    return render(request, 'main/checklist.html',
                  {'task_group_list': task_group_list, 'task_group_form': task_group_form, 'error': error})


@login_required(login_url='login')
def add_new_subtask(request):
    task_group_id = request.POST['task_group_id']
    subtask_description = request.POST['subtask-description']

    Task(task_group=TaskGroup.objects.filter(id=task_group_id)[0], description=subtask_description).save()
    return redirect('checklist')


# class SubtaskUpdateView(UpdateView):
#     model = Task
#     template_name = 'main/checklist.html'
#
#     form_class = TaskForm


# def update_subtask(request):
#     task_group_id = request.POST.get['task_group_id']
#     subtask_description = request.POST.get['subtask-description']
#     task = Task.objects.get(task_group=TaskGroup.objects.filter(id=task_group_id)[0], description=subtask_description)
#     form = TaskForm(instance=task)
#
#     context = {'form':form}
#     return render(request, 'main/checklist.html', context)

@login_required(login_url='login')
def handle_task(request):
    status = request.POST['status']
    id = request.POST['id']

    task = Task.objects.filter(id=id)[0]
    task.status = status
    task.save()

    return JsonResponse({})


def budget(request):
    context = {}
    return render(request, 'main/budget.html', context)


def project_list(request):
    context = {}
    return render(request, 'main/project_list.html', context)


def project_detail(request, project_slug):

    project = get_object_or_404(Project, slug=project_slug)
    context = {'project' : project, 'expense_list' : project.expenses.all()}
    return render(request, 'main/budget.html', context)