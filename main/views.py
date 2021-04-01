from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.utils.text import slugify

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


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'main/create_project.html'
    fields = ('name', 'bride_name', 'groom_name', 'wedding_date', 'ceremony_place', 'budget')

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return slugify(self.request.POST['name'])

@login_required(login_url='login')
def guests(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    bride_side_guests = project.guests.filter(side="B")
    groom_side_guests = project.guests.filter(side="G")

    bride_side_amount = project.guests.filter(side="B").count()
    groom_side_amount = project.guests.filter(side="G").count()

    total_male = project.guests.filter(sex="M").count()
    total_female = project.guests.filter(sex="F").count()
    total_child = project.guests.filter(sex="C").count()

    return render(request, 'main/guests.html',
                  {'project': project, 'bride_side_guests': bride_side_guests, 'groom_side_guests': groom_side_guests,
                   'bride_side_amount': bride_side_amount, 'groom_side_amount': groom_side_amount,
                   'total_male': total_male, 'total_female': total_female, 'total_child': total_child})


@login_required(login_url='login')
def overview(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, user=request.user)
    context = {'project': project}
    return render(request, 'main/overview.html', context)


@login_required(login_url='login')
def checklist(request, project_slug):
    # data = {
    #     'title': 'Online Wedding Planner | Список дел'
    # }
    project = get_object_or_404(Project, slug=project_slug, user=request.user)
    error = ''
    if request.method == "POST":
        task_group_form = TaskGroupForm(request.POST)
        # task_group_form.instance.user = User.objects.get(id=1)
        task_group_form.instance.project = Project.objects.get(id=1)

        if task_group_form.is_valid():
            task_group_form.save()
            return redirect('checklist', project_slug)
        else:
            error = 'Данные введены некорректно'

    if request.user.is_authenticated:
        # task_group_list = TaskGroup.objects.filter(user=request.user)
        task_group_list = project.task_group.all()
    else:
        task_group_list = []
    tasks = Task.objects.all()

    for group in task_group_list:
        group.tasks = list(filter(lambda task: task.task_group == group, tasks))
        task_form = TaskForm()
        group.task_form = task_form

    task_group_form = TaskGroupForm()

    return render(request, 'main/checklist.html',
                  {'project': project, 'task_group_list': task_group_list, 'task_group_form': task_group_form,
                   'error': error})


@login_required(login_url='login')
def add_new_subtask(request, project_slug):
    task_group_id = request.POST['task_group_id']
    subtask_description = request.POST['subtask-description']

    Task(task_group=TaskGroup.objects.filter(id=task_group_id)[0], description=subtask_description).save()
    return redirect('checklist', project_slug)


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
def handle_task(request, project_slug):
    status = request.POST['status']
    id = request.POST['id']

    task = Task.objects.filter(id=id)[0]
    task.status = status
    task.save()

    return JsonResponse({})


def create_project(request):
    context = {}
    return render(request, 'main/create_project.html', context)


def budget(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, user=request.user)
    context = {'project': project, 'expense_list': project.expenses.all()}
    return render(request, 'main/budget.html', context)
