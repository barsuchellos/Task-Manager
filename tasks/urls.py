from django.urls import path

from tasks import views

app_name = "tasks"

urlpatterns = [
    path("", views.index, name="index"),
    path("registration/", views.worker_create, name="registration"),
    path("tasks/", views.task_list, name="task-list"),
    path("workers/", views.worker_list, name="worker-list"),
    path("positions/", views.positions_list, name="position-list"),
    path("task-types/", views.task_type_list, name="task-type-list"),
    path("tasks/create/", views.task_create, name="task-create"),
    path("tasks/<int:pk>/", views.task_detail, name="task-detail"),
    path("tasks/<int:pk>/update/", views.task_update, name="task-update"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task-delete"),
    path("tasks/<int:pk>/toggle/", views.task_toggle, name="task-toggle"),
    path("workers/update/", views.worker_update_view, name="worker-update"),
    path("workers/<int:pk>/", views.worker_detail, name="worker-detail"),
    path("positions/create/", views.position_create, name="position-create"),
    path("task-types/create/", views.task_type_create, name="task-type-create"),
]
