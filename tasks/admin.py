from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import TaskType, Worker, Task, Position, Team


@admin.register(TaskType)
class AdminTaskType(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Position)
class AdminPosition(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display = ("name", "description", "deadline", "is_completed", "priority", "task_type",)
    search_fields = ("name", "priority", "description",)
    list_filter = ("is_completed", "priority",)
    ordering = ("name",)


@admin.register(Worker)
class AdminWorker(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    search_fields = ("username", "position", "email")
    fieldsets = UserAdmin.fieldsets + (("Position", {"fields": ("position",)}),)

@admin.register(Team)
class AdminTeam(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("members",)
