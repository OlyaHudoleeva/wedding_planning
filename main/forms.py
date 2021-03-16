from django.forms import ModelForm, TextInput

from .models import *


class TaskGroupForm(ModelForm):
    class Meta:
        model = TaskGroup
        fields = ['name']

        widgets = {
            "name": TextInput(attrs={
                'class' : 'form-control task-list-name',
                'name' : 'task-group-name',
                'type': 'text',
                'id': 'add-new-task-group',
                'placeholder': 'Придумайте название новой группы задач...',
                'aria-label': 'Придумайте название новой группы задач...',
                'aria-describedby': 'button-addon2'
            })
        }

