from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=20)
#     surname = models.CharField(max_length=30)
#     email = models.CharField(max_length=20)
#     login = models.CharField(max_length=50)
#     password = models.CharField(max_length=20)

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    bride_name = models.CharField(max_length=20)
    groom_name = models.CharField(max_length=20)
    wedding_date = models.DateField(blank=True)
    ceremony_place = models.CharField(max_length=200, blank=True)
    budget = models.IntegerField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def budget_left(self):
        expense_list = Expense.objects.filter(project=self)
        total_expense_cost = 0
        for expense in expense_list:
            total_expense_cost += expense.cost
        return self.budget - total_expense_cost

    def total_prepayment(self):
        expense_list = Expense.objects.filter(project=self)
        total_prepayment = 0
        for expense in expense_list:
            total_prepayment += expense.prepayment
        return total_prepayment




class TaskGroup(models.Model):
    STATUS = (
        ('P', 'В процессе'),
        ('C', 'Выполнена'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='task_group')
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

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='guests')
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


class Category(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория расходов'
        verbose_name_plural = 'Категории расходов'


class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=60)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    prepayment = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'

    # def payment_left(self):
    #     expense_list = Expense.objects.filter(project=self)
    #     return self.cost - self.prepayment
