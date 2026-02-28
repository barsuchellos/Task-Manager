from datetime import date

from django.test import TestCase

from tasks.models import TaskType, Position, Task, Worker


class PositionModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Developer."
        )

    def test_position_str(self):
        self.assertEqual(str(self.position), "Developer.")


class TaskTypeModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="Refactoring."
        )

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Refactoring.")


class TaskModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")
        self.worker = Worker.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.task = Task.objects.create(
            name="Fix login bug",
            description="Some description",
            deadline=date(2026, 12, 31),
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
        )
        self.task.assignees.set([self.worker])

    def test_task_str(self):
        self.assertEqual(str(self.task), "Fix login bug")

    def test_task_default_is_completed(self):
        self.assertFalse(self.task.is_completed)

    def test_task_default_priority(self):
        task = Task.objects.create(
            name="No priority task",
            deadline=date(2026, 12, 31),
            task_type=self.task_type,
        )
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

    def test_task_assignees(self):
        self.assertIn(self.worker, self.task.assignees.all())


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="john",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            position=self.position,
        )

    def test_worker_str_with_position(self):
        self.assertEqual(str(self.worker), "john (Developer)")

    def test_worker_str_without_position(self):
        worker = Worker.objects.create_user(
            username="noposition",
            password="testpass123",
        )
        self.assertEqual(str(worker), "noposition (None)")

    def test_worker_position(self):
        self.assertEqual(self.worker.position, self.position)

    def test_worker_position_set_null_on_delete(self):
        self.position.delete()
        self.worker.refresh_from_db()
        self.assertIsNone(self.worker.position)
