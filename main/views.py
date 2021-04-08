import xlwt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import escape_uri_path
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user
from .forms import *
from .models import *


@unauthenticated_user
def register_page(request):

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


@unauthenticated_user
def login_page(request):
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
    # project = get_object_or_404(Project, user=request.user)

    context = {}
    return render(request, 'main/index.html', context)


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


def project_list(request):
    project_list = Project.objects.filter(user=request.user)
    context = {'project_list': project_list}

    return render(request, 'main/project_list.html', context)


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

    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            sex = form.cleaned_data['sex']
            side = form.cleaned_data['side']

            Guest.objects.create(
                project=project,
                first_name=first_name,
                last_name=last_name,
                sex=sex,
                side=side
            ).save()
            return HttpResponseRedirect('guests', project_slug)

    return render(request, 'main/guests.html',
                  {'project': project, 'bride_side_guests': bride_side_guests, 'groom_side_guests': groom_side_guests,
                   'bride_side_amount': bride_side_amount, 'groom_side_amount': groom_side_amount,
                   'total_male': total_male, 'total_female': total_female, 'total_child': total_child})


def delete_guest(request, project_slug):
    id = request.POST['id']
    Guest(id=id).delete()

    return redirect('guests', project_slug)


def export_excel(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, user=request.user)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + escape_uri_path('Список гостей') + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Список гостей')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['RSVP', 'Имя', 'Фамилия', 'Сторона']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = project.guests.all().values_list('rsvp', 'first_name', 'last_name', 'side')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


@login_required(login_url='login')
def overview(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, user=request.user)

    # completed_tasks = Task.objects.filter(status="C").count()
    # все в бд выполненные задачи

    # completed_tasks = 0


    # таск группы проекта

    all_tasks_num = Task.objects.all().count() # все в бд задачи

    task_groups = project.task_group.all() #все таск группы проекта
    tasks = Task.objects.all()

    total_tasks_amount = 0
    completed_tasks_amount = 0

    for group in task_groups:
        group.tasks = list(filter(lambda task: task.task_group == group, tasks))
        total_tasks_amount += len(group.tasks)
        completed_tasks_amount += len(list(filter(lambda task: task.status == "C", group.tasks)))


    context = {'project': project, 'completed_tasks_amount': completed_tasks_amount, 'total_tasks_amount': total_tasks_amount}
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
        task_group_form.instance.project = Project.objects.get(id=project.id)

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
    project = get_object_or_404(Project, slug=project_slug, user=request.user)
    # project_slug = request.POST['project.slug']

    status = request.POST['status']
    id = request.POST['id']

    task = Task.objects.filter(id=id)[0]
    task.status = status
    task.save()

    context = {'project':project}
    return render(request, 'main/checklist.html', context)
    # return JsonResponse({})



def create_project(request):
    context = {}
    return render(request, 'main/create_project.html', context)


def budget(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, user=request.user)

    expense_list = project.expenses.all()

    for expense in expense_list:
        expense.payment_left = expense.cost - expense.prepayment

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            cost = form.cleaned_data['cost']
            prepayment = form.cleaned_data['prepayment']

            Expense.objects.create(
                project=project,
                description=description,
                cost=cost,
                prepayment=prepayment
            ).save()
            return HttpResponseRedirect('budget', project_slug)

    context = {'project': project, 'expense_list': expense_list}
    return render(request, 'main/budget.html', context)


def delete_expense(request, project_slug):
    id = request.POST['id']
    Expense(id=id).delete()

    return redirect('budget', project_slug)
