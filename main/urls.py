from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.register_page, name='registration'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),

    path('projects', views.project_list, name='project_list'),
    path('<slug:project_slug>', views.project_detail, name='project_detail'),

    path('', views.index, name='home'),
    path('guests', views.guests, name='guests'),
    path('overview', views.overview, name='overview'),
    path('checklist', views.checklist, name='checklist'),

    path('add_new_subtask', views.add_new_subtask, name='add_new_subtask'),
    # path('update_subtask', views.update_subtask, name = 'update_subtask'),
    path('handle_task', views.handle_task),

    path('budget', views.budget, name='budget'),

    # path('create_task_group', views.createTaskGroup, name='create_task_group')
    # path('add_tasks', views.add_tasks)
]
