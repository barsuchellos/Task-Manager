from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import TaskType, Worker, Task, Position


@admin.register(TaskType)
class AdminTaskType(admin.ModelAdmin):
    pass

@admin.register(Position)
class AdminPosition(admin.ModelAdmin):
    pass

@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    pass

@admin.register(Worker)
class AdminWorker(UserAdmin):
    pass
