from django.contrib.auth import get_user_model

from tasks.models import Task, Position, TaskType


def create_task(data):
    task = Task.objects.create(
        name=data["name"],
        description=data["description"],
        deadline=data["deadline"],
        priority=data["priority"],
        task_type=data["task_type"],
        team=data["team"],
    )

    task.assignees.set(data["assignees"])
    return task


def update_task(task, data):
    task.description = data["description"]
    task.deadline = data["deadline"]
    task.priority = data["priority"]
    task.task_type = data["task_type"]
    task.team = data["team"]

    task.save()
    task.assignees.set(data["assignees"])


def delete_task(task):
    task.delete()


def task_toggle_update(task):
    task.is_completed = not task.is_completed
    task.save()


def create_workers(user):
    worker = get_user_model().objects.create_user(
        username=user["username"],
        password=user["password1"],
        email=user["email"],
        position=user["position"],
        first_name=user["first_name"],
        last_name=user["last_name"],
    )

    return worker


def worker_update(worker, form_data):
    worker.username = form_data["username"]
    if form_data["new_password"]:
        worker.set_password(form_data["new_password"])
    worker.email = form_data["email"]
    worker.position = form_data["position"]
    worker.first_name = form_data["first_name"]
    worker.last_name = form_data["last_name"]

    worker.save()

def create_positions(form):
    return Position.objects.create(
        name=form["name"]
    )

def create_task_types(form):
    return TaskType.objects.create(
        name=form["name"]
    )

