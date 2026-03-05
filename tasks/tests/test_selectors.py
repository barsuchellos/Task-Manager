from datetime import date, timedelta

from django.test import TestCase

from tasks.models import Task, TaskType, Worker, Position, Team
from tasks.selectors import (
    get_all_tasks,
    get_task,
    get_worker_tasks,
    get_urgent_tasks,
    get_total_workers,
    get_all_task_types,
    get_workers,
    get_worker_by_id,
    get_positions,
    get_task_types_list
)


class ServiceTests(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Developer")

        self.worker = Worker.objects.create_user(
            username="worker1",
            password="test123",
            position=self.position
        )

        self.team = Team.objects.create(name="Backend Team")
        self.team.members.add(self.worker)

        self.task_type = TaskType.objects.create(name="Bug")

        self.task = Task.objects.create(
            name="Fix login bug",
            task_type=self.task_type,
            team=self.team,
            deadline=date.today() + timedelta(days=3),
            priority=Task.Priority.URGENT,
            is_completed=False
        )

        self.task.assignees.add(self.worker)

    def test_get_all_tasks(self):
        tasks = get_all_tasks(self.worker)
        self.assertEqual(tasks.count(), 1)

    def test_get_task(self):
        task = get_task(self.worker, self.task.id)
        self.assertEqual(task.id, self.task.id)

    def test_get_worker_tasks(self):
        stats = get_worker_tasks(self.worker)

        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["urgent_tasks"], 1)

    def test_get_urgent_tasks(self):
        tasks = get_urgent_tasks(self.worker)
        self.assertEqual(tasks.count(), 1)

    def test_get_total_workers(self):
        total = get_total_workers(self.worker)
        self.assertEqual(total, 1)

    def test_get_all_task_types(self):
        types = get_all_task_types(self.worker)
        self.assertEqual(types.count(), 1)

    def test_get_workers(self):
        workers = get_workers(self.worker)
        self.assertEqual(workers.count(), 1)

    def test_get_worker_by_id(self):
        worker = get_worker_by_id(self.worker, self.worker.id)
        self.assertEqual(worker.id, self.worker.id)

    def test_get_positions(self):
        positions = get_positions()
        self.assertEqual(positions.count(), 1)

    def test_get_task_types_list(self):
        types = get_task_types_list()
        self.assertEqual(types.count(), 1)
