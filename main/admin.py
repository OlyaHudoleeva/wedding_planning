from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Task)
admin.site.register(TaskGroup)
admin.site.register(Guest)
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Expense)