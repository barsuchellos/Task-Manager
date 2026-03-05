from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from tasks.models import Task, TaskType, Worker, Position, Team


class ViewTests(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Developer")

        self.user = Worker.objects.create_user(
            username="testuser",
            password="test123",
            position=self.position
        )

        self.client.login(username="testuser", password="test123")

        self.team = Team.objects.create(name="Backend")
        self.team.members.add(self.user)

        self.task_type = TaskType.objects.create(name="Bug")

        self.task = Task.objects.create(
            name="Fix bug",
            description="desc",
            deadline=date.today() + timedelta(days=2),
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type,
            team=self.team,
        )

        self.task.assignees.add(self.user)

    def test_index_page(self):
        response = self.client.get(reverse("tasks:index"))

        self.assertEqual(response.status_code, 200)

    def test_task_list(self):
        response = self.client.get(reverse("tasks:task-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_detail(self):
        response = self.client.get(
            reverse("tasks:task-detail", args=[self.task.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_task_create(self):
        data = {
            "name": "New Task",
            "description": "Test",
            "deadline": date.today(),
            "priority": Task.Priority.HIGH,
            "task_type": self.task_type.id,
            "team": self.team.id,
            "assignees": [self.user.id],
        }

        response = self.client.post(
            reverse("tasks:task-create"),
            data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_update(self):
        data = {
            "name": "Fix bug",
            "description": "updated",
            "deadline": date.today(),
            "priority": Task.Priority.HIGH,
            "task_type": self.task_type.id,
            "team": self.team.id,
            "assignees": [self.user.id],
        }

        response = self.client.post(
            reverse("tasks:task-update", args=[self.task.id]),
            data
        )

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.task.description, "updated")

    def test_task_delete(self):
        response = self.client.post(
            reverse("tasks:task-delete", args=[self.task.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_toggle(self):
        response = self.client.get(
            reverse("tasks:task-toggle", args=[self.task.id])
        )

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.task.is_completed)

    def test_worker_list(self):
        response = self.client.get(reverse("tasks:worker-list"))

        self.assertEqual(response.status_code, 200)

    def test_worker_detail(self):
        response = self.client.get(
            reverse("tasks:worker-detail", args=[self.user.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_positions_list(self):
        response = self.client.get(reverse("tasks:position-list"))

        self.assertEqual(response.status_code, 200)

    def test_task_type_list(self):
        response = self.client.get(reverse("tasks:task-type-list"))

        self.assertEqual(response.status_code, 200)
