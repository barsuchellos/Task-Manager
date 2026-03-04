from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Task Type"
        verbose_name_plural = "Task Types"

    def __str__(self) -> str:
        return f"{self.name}"


class Position(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self) -> str:
        return f"{self.name}"


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "urgent", "Urgent"
        HIGH = "high", "High"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    task_type = models.ForeignKey(
        to=TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        to="Worker",
        related_name="tasks"
    )
    team = models.ForeignKey(
        "Team",
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["deadline", "name"]
        verbose_name_plural = "Tasks"

    def __str__(self) -> str:
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(
        to=Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers"
    )

    class Meta:
        verbose_name_plural = "Workers"

    def __str__(self) -> str:
        return f"{self.username} ({self.position})"


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(
        Worker,
        related_name="teams",
        blank=True
    )

    def __str__(self):
        return self.name
