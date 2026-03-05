from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from tasks.forms import TaskCreateForm, TaskUpdateForm, WorkerRegistrationForm, FormWorkerUpdate, PositionCreateForm, \
    TaskTypesCreateForm, TaskFilterForm
from tasks.selectors import get_all_tasks, get_task, get_workers, get_worker_by_id, get_worker_tasks, get_total_workers, \
    get_urgent_tasks, get_positions, get_task_types_list
from tasks.services import create_task, update_task, delete_task, task_toggle_update, create_workers, worker_update, \
    create_positions, create_task_types


def index(request) -> HttpResponse:
    if request.user.is_authenticated:
        context = {
            "info_tasks": get_worker_tasks(request.user),
            "info_workers": get_total_workers(request.user),
            "info_urgent_tasks": get_urgent_tasks(request.user)
        }
        return render(request, "tasks/dashboard.html", context=context)
    return render(request, "tasks/index.html", {})


@login_required
def task_list(request) -> HttpResponse:
    form = TaskFilterForm(request.GET, user=request.user)
    print("form.errors", form.errors)
    print("form.is_valid()", form.is_valid())
    print("request.GET.getlist(workers)",request.GET.getlist("workers"))
    if form.is_valid():
        tasks = get_all_tasks(
            user=request.user,
            task_name=form.cleaned_data.get("task_name"),
            task_type=form.cleaned_data.get("task_type"),
            worker=form.cleaned_data.get("workers")
        )
    else:
        tasks = get_all_tasks(request.user)

    print("selected_workers", request.GET.getlist("workers"))
    paginator = Paginator(tasks, 7)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "tasks": page_obj,
        "form": form,
        "page_obj": page_obj,
        "selected_workers": request.GET.getlist("workers"),
    }

    return render(request, "tasks/task_list.html", context=context)


@login_required
def task_detail(request, pk):
    task = get_task(request.user, pk)
    context = {"task": task}
    return render(request, "tasks/task_detail.html", context=context)


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            create_task(data=form.cleaned_data)
            return redirect("tasks:task-list")
        else:
            context = {"form": form}
            return render(request, "tasks/task_create.html", context=context)
    else:
        form = TaskCreateForm()
        context = {"form": form}
        return render(request, "tasks/task_create.html", context=context)


@login_required
def task_update(request, pk):
    task = get_task(request.user, pk)

    if request.method == "POST":
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            update_task(task, data=form.cleaned_data)
            return redirect("tasks:task-detail", pk=pk)
        else:
            context = {"form": form, "task": task}
            return render(request, "tasks/task_update.html", context=context)
    else:
        form = TaskUpdateForm(instance=task)
        context = {
            "form": form,
            "task": task
        }
        return render(request, "tasks/task_update.html", context=context)


@login_required
def task_delete(request, pk):
    task = get_task(request.user, pk)

    if request.method == "POST":
        delete_task(task)
        return redirect("tasks:task-list")
    else:
        return render(request, "tasks/task_confirm_delete.html", {"task": task})


@login_required
def task_toggle(request, pk):
    print("request::", request, pk)
    task = get_task(request.user, pk)

    task_toggle_update(task)
    return redirect("tasks:task-detail", pk=pk)


@login_required
def worker_list(request):
    workers = get_workers(request.user)
    context = {"workers": workers}

    return render(request, "tasks/workers_list.html", context=context)


@login_required
def task_type_list(request):
    task_types_list = get_task_types_list()
    context = {"types_list": task_types_list}
    return render(request, "tasks/task_types_list.html", context=context)


@login_required
def worker_detail(request, pk):
    worker = get_worker_by_id(request.user, pk)
    return render(request, "tasks/worker_details.html", {"worker": worker})


def worker_create(request):
    if request.user.is_authenticated:
        return redirect("tasks:index")
    form = WorkerRegistrationForm()
    if request.method == "POST":
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            create_workers(form.cleaned_data)
            return redirect("tasks:index")
        else:
            context = {"form": form}
            return render(request, "tasks/registration.html", context=context)
    return render(request, "tasks/registration.html", {"form": form})


@login_required
def worker_update_view(request):
    if request.method == "POST":
        form = FormWorkerUpdate(request.POST, instance=request.user)

        if form.is_valid():
            worker_update(request.user, form.cleaned_data)
            update_session_auth_hash(request, request.user)
            return redirect('tasks:worker-detail', pk=request.user.pk)
        else:
            return render(request, "tasks/worker_update.html", {"form": form})
    else:
        form = FormWorkerUpdate(instance=request.user)
        return render(request, "tasks/worker_update.html", {"form": form})


@login_required
def positions_list(request):
    positions = get_positions()
    context = {"positions": positions}
    return render(request, "tasks/positions_list.html", context=context)


def position_create(request):
    if request.method == "POST":
        form = PositionCreateForm(request.POST)
        if form.is_valid():
            create_positions(form.cleaned_data)
            return redirect("tasks:position-list")
        else:
            context = {"form": form}
            return render(request, "tasks/positions_create.html", context=context)
    return render(request, "tasks/positions_create.html", {"form": PositionCreateForm()})


def task_type_create(request):
    form = TaskTypesCreateForm()

    if request.method == "POST":
        form = TaskTypesCreateForm(request.POST)
        if form.is_valid():
            create_task_types(form.cleaned_data)
            return redirect("tasks:task-type-list")
        else:
            return render(request, "tasks/task_types_create.html", context={"form": form})
    return render(request, "tasks/task_types_create.html", context={"form": form})
