from datetime import date

from django.db.models import Count
from django.db.models import Q
from django.shortcuts import get_object_or_404

from tasks.models import Task, TaskType, Worker, Position


def get_all_tasks(user, task_name=None, task_type=None, worker=None):
    tasks_by_team = Task.objects.filter(team__members=user)
    tasks_by_assignee = Task.objects.filter(assignees=user)
    result = (tasks_by_team | tasks_by_assignee)

    if task_name:
        result = result.filter(name__icontains=task_name)
    if task_type:
        result = result.filter(task_type=task_type)
    if worker:
        result = result.filter(assignees__id__in=worker)

    return result.select_related("task_type").prefetch_related("assignees").distinct()


def get_task(user, pk):
    return get_object_or_404(
        Task.objects.filter(
            Q(team__members=user) | Q(assignees=user)
        ).distinct(),
        pk=pk
    )


def get_worker_tasks(user):
    task = Task.objects.filter(Q(team__members=user) | Q(assignees=user)).distinct()
    return task.aggregate(
        total=Count("id"),
        completed=Count("id", filter=Q(is_completed=True)),
        pending_tasks=Count("id", filter=Q(deadline__gt=date.today())),
        overdue_tasks=Count("id", filter=(Q(deadline__lt=date.today()) & Q(is_completed=False))),
        urgent_tasks=Count("id", filter=Q(priority="urgent")),
    )


def get_urgent_tasks(user):
    return Task.objects.filter(
        Q(team__members=user) | Q(assignees=user),
        priority="urgent",
        is_completed=False
    ).distinct()


def get_total_workers(user):
    return Worker.objects.filter(teams__members=user).distinct().count()


def get_all_task_types(user):
    return TaskType.objects.all()


def get_workers(user):
    return ((Worker.objects
             .filter(teams__members=user)
             .select_related("position")
             .prefetch_related("teams"))
            .distinct())


def get_worker_by_id(user, pk):
    return get_object_or_404(
        Worker.objects.filter(teams__members=user).distinct(), id=pk
    )


def get_positions():
    return Position.objects.all()


def get_task_types_list():
    return TaskType.objects.all()
