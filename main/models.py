from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=20)
#     surname = models.CharField(max_length=30)
#     email = models.CharField(max_length=20)
#     login = models.CharField(max_length=50)
#     password = models.CharField(max_length=20)

class TaskGroup(models.Model):
    STATUS = (
        ('P', 'In progress'),
        ('C', 'Completed'),
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS, default='P')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Список задач'
        verbose_name_plural = 'Списки задач'


class Task(models.Model):
    STATUS = (
        ('P', 'In progress'),
        ('C', 'Completed'),
    )
    task_group_id = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
