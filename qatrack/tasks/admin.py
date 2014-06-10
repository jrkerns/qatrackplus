from django.contrib import admin
from qatrack.tasks.models import Category, Task

admin.site.register(Category)
admin.site.register(Task)