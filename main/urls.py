from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('guests', views.guests, name='guests'),
    path('overview', views.overview, name='overview'),
    path('checklist', views.checklist, name='checklist'),
    # path('create_task_group', views.createTaskGroup, name='create_task_group')
    # path('add_tasks', views.add_tasks)
]
