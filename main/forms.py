from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, PasswordInput, EmailInput
from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control my-2 p-4',
                'placeholder': 'Имя пользователя'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control my-2 p-4',
                'placeholder': 'Адрес электронной почты'
            }),
            'password1': PasswordInput(attrs={
                'class': 'form-control my-2 p-4',
                'placeholder': 'Пароль'
            }),
            'password2': PasswordInput(attrs={
                'class': 'form-control my-2 p-4',
                'placeholder': 'Повторите пароль'
            }),
        }


class TaskGroupForm(ModelForm):
    class Meta:
        model = TaskGroup
        fields = ['name']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control task-list-name',
                'name': 'task-group-name',
                'id': 'add-new-task-group',
                'placeholder': 'Придумайте название новой группы задач...',
                'aria-label': 'Придумайте название новой группы задач...',
                'aria-describedby': 'button-addon2'
            })
        }


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['description']


class ExpenseForm(forms.Form):
    description = forms.CharField()
    cost = forms.DecimalField(decimal_places=2)
    prepayment = forms.DecimalField(decimal_places=2)


SEX_CHOISES = ((
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        ('C', 'Ребёнок'),
    ))

SIDE_CHOISES = ((
        ('G', 'Сторона жениха'),
        ('B', 'Сторона невесты'),
    ))

class GuestForm(forms.Form):
    first_name = forms.CharField(label="Имя гостя", max_length=20)
    last_name = forms.CharField(label="Фамилия гостя", max_length=20)
    sex = forms.ChoiceField(choices=SEX_CHOISES, widget=forms.RadioSelect)
    side = forms.ChoiceField(choices=SIDE_CHOISES, widget=forms.RadioSelect)


