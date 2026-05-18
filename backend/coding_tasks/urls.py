from django.urls import path
from . import views

app_name = "coding_tasks"

urlpatterns = [

    # Trainer
    path(
        "create/",
        views.create_task,
        name="create_task"
    ),

    # Student
    path(
        "tasks/",
        views.available_tasks,
        name="available_tasks"
    ),

    path(
        "submit/<int:task_id>/",
        views.submit_task,
        name="submit_task"
    ),

    path(
        "my-submissions/",
        views.my_submissions,
        name="my_submissions"
    ),
]