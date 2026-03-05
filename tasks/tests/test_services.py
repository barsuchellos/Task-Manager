from datetime import date, timedelta

from django.test import TestCase

from tasks.models import Task, TaskType, Worker, Position, Team
from tasks.services import (
    create_task,
    update_task,
    delete_task,
    task_toggle_update,
    create_workers,
    worker_update,
    create_positions,
    create_task_types,
)


class ServiceTests(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Developer")

        self.worker = Worker.objects.create_user(
            username="worker1",
            password="test123",
            position=self.position
        )

        self.team = Team.objects.create(name="Team A")
        self.team.members.add(self.worker)

        self.task_type = TaskType.objects.create(name="Bug")

        self.task = Task.objects.create(
            name="Initial task",
            description="test",
            deadline=date.today() + timedelta(days=2),
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type,
            team=self.team,
        )

        self.task.assignees.add(self.worker)

    def test_create_task(self):
        data = {
            "name": "New task",
            "description": "description",
            "deadline": date.today(),
            "priority": Task.Priority.HIGH,
            "task_type": self.task_type,
            "team": self.team,
            "assignees": [self.worker],
        }

        task = create_task(data)

        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(task.name, "New task")
        self.assertEqual(task.assignees.first(), self.worker)

    def test_update_task(self):
        new_type = TaskType.objects.create(name="Feature")

        data = {
            "description": "updated description",
            "deadline": date.today(),
            "priority": Task.Priority.HIGH,
            "task_type": new_type,
            "team": self.team,
            "assignees": [self.worker],
        }

        update_task(self.task, data)

        self.task.refresh_from_db()

        self.assertEqual(self.task.description, "updated description")
        self.assertEqual(self.task.priority, Task.Priority.HIGH)

    def test_delete_task(self):
        delete_task(self.task)

        self.assertEqual(Task.objects.count(), 0)

    def test_task_toggle_update(self):
        self.assertFalse(self.task.is_completed)

        task_toggle_update(self.task)

        self.task.refresh_from_db()

        self.assertTrue(self.task.is_completed)

    def test_create_workers(self):
        data = {
            "username": "new_worker",
            "password1": "password123",
            "email": "test@test.com",
            "position": self.position,
            "first_name": "John",
            "last_name": "Doe",
        }

        worker = create_workers(data)

        self.assertEqual(Worker.objects.count(), 2)
        self.assertEqual(worker.username, "new_worker")

    def test_worker_update(self):
        data = {
            "username": "updated_user",
            "new_password": "newpass123",
            "email": "new@mail.com",
            "position": self.position,
            "first_name": "Jane",
            "last_name": "Smith",
        }

        worker_update(self.worker, data)

        self.worker.refresh_from_db()

        self.assertEqual(self.worker.username, "updated_user")
        self.assertEqual(self.worker.first_name, "Jane")

    def test_create_positions(self):
        form = {"name": "Manager"}

        position = create_positions(form)

        self.assertEqual(Position.objects.count(), 2)
        self.assertEqual(position.name, "Manager")

    def test_create_task_types(self):
        form = {"name": "Improvement"}

        task_type = create_task_types(form)

        self.assertEqual(TaskType.objects.count(), 2)
        self.assertEqual(task_type.name, "Improvement")
