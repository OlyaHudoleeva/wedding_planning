from django.urls import path

from . import views


urlpatterns = [
    path('registration', views.register_page, name='registration'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),

    path('create_project', views.ProjectCreateView.as_view(), name='create_project'),
    path('project_list', views.project_list, name='project_list'),

    path('', views.index, name='home'),

    path('<slug:project_slug>', views.overview, name='overview'),

    path('<slug:project_slug>/guests', views.guests, name='guests'),
    path('<slug:project_slug>/delete_guest', views.delete_guest, name='delete_guest'),
    path('<slug:project_slug>/export_excel', views.export_excel, name='export_excel'),

    path('<slug:project_slug>/checklist', views.checklist, name='checklist'),
    path('<slug:project_slug>/add_new_subtask', views.add_new_subtask, name='add_new_subtask'),
    path('<slug:project_slug>/handle_task', views.handle_task),

    path('<slug:project_slug>/budget', views.budget, name='budget'),
    path('<slug:project_slug>/delete_expense', views.delete_expense, name='delete_expense')



    # path('update_subtask', views.update_subtask, name = 'update_subtask'),
    # path('create_task_group', views.createTaskGroup, name='create_task_group')
    # path('add_tasks', views.add_tasks)
]
