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
        ('P', 'В процессе'),
        ('C', 'Выполнена'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS, default='P')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Список задач'
        verbose_name_plural = 'Списки задач'


class Task(models.Model):
    STATUS = (
        ('P', 'В процессе'),
        ('C', 'Выполнена'),
    )
    task_group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Guest(models.Model):
    SEX = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        ('C', 'Ребёнок'),
    )

    RSVP = (
        ('IN', 'Приглашение не отправлено'),
        ('IS', 'Приглашение отправлено'),
        ('IA', 'Приглашение принято'),
        ('ID', 'Приглашение отклонено'),
    )

    SIDE = (
        ('G', 'Сторона жениха'),
        ('B', 'Сторона невесты')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    sex = models.CharField(max_length=1, choices=SEX, default='M')
    rsvp = models.CharField(max_length=2, choices=RSVP, default='IN')
    side = models.CharField(max_length=1, choices=SIDE, default='B')


    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'