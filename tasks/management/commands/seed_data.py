from datetime import date, timedelta

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from tasks.models import Task, Worker, Position, TaskType, Team


class Command(BaseCommand):
    help = "Seed database with test data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Positions
        positions_data = ["Backend Developer", "Frontend Developer", "QA Engineer", "Project Manager", "DevOps"]
        positions = []
        for name in positions_data:
            position, _ = Position.objects.get_or_create(name=name)
            positions.append(position)
        self.stdout.write("✓ Positions created")

        # Task Types
        task_types_data = ["Bug", "Feature", "Refactoring", "Documentation", "Testing", "DevOps"]
        task_types = []
        for name in task_types_data:
            task_type, _ = TaskType.objects.get_or_create(name=name)
            task_types.append(task_type)
        self.stdout.write("✓ Task types created")

        # Workers
        workers_data = [
            {"username": "john_dev", "first_name": "John", "last_name": "Smith", "email": "john@example.com",
             "position": positions[0]},
            {"username": "jane_front", "first_name": "Jane", "last_name": "Doe", "email": "jane@example.com",
             "position": positions[1]},
            {"username": "mike_qa", "first_name": "Mike", "last_name": "Johnson", "email": "mike@example.com",
             "position": positions[2]},
            {"username": "sarah_pm", "first_name": "Sarah", "last_name": "Williams", "email": "sarah@example.com",
             "position": positions[3]},
            {"username": "alex_ops", "first_name": "Alex", "last_name": "Brown", "email": "alex@example.com",
             "position": positions[4]},
            {"username": "kate_dev", "first_name": "Kate", "last_name": "Davis", "email": "kate@example.com",
             "position": positions[0]},
        ]
        workers = []
        for data in workers_data:
            worker, created = Worker.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "position": data["position"],
                    "password": make_password("password123"),
                }
            )
            workers.append(worker)
        self.stdout.write("✓ Workers created")

        # Teams
        teams_data = [
            {"name": "Backend Team", "members": [workers[0], workers[5], workers[2]]},
            {"name": "Frontend Team", "members": [workers[1], workers[3]]},
            {"name": "Infrastructure Team", "members": [workers[4], workers[0]]},
        ]
        teams = []
        for data in teams_data:
            team, _ = Team.objects.get_or_create(name=data["name"])
            team.members.set(data["members"])
            teams.append(team)
        self.stdout.write("✓ Teams created")

        # Tasks
        tasks_data = [
            # Backend Team tasks
            {"name": "Fix authentication bug", "description": "Users cannot login with special characters in password",
             "priority": "urgent", "task_type": task_types[0], "team": teams[0], "assignees": [workers[0]], "days": 2},
            {"name": "Implement JWT refresh token", "description": "Add refresh token logic to auth service",
             "priority": "high", "task_type": task_types[1], "team": teams[0], "assignees": [workers[0], workers[5]],
             "days": 7},
            {"name": "Refactor user service", "description": "Split user service into smaller modules",
             "priority": "medium", "task_type": task_types[2], "team": teams[0], "assignees": [workers[5]], "days": 14},
            {"name": "Write API documentation", "description": "Document all REST endpoints using Swagger",
             "priority": "low", "task_type": task_types[3], "team": teams[0], "assignees": [workers[0]], "days": 10},
            {"name": "Fix database N+1 queries", "description": "Optimize slow queries on task list page",
             "priority": "high", "task_type": task_types[0], "team": teams[0], "assignees": [workers[5], workers[0]],
             "days": 3},
            {"name": "Add pagination to API", "description": "Implement cursor-based pagination", "priority": "medium",
             "task_type": task_types[1], "team": teams[0], "assignees": [workers[0]], "days": 5},
            {"name": "Write unit tests for services", "description": "Cover all service functions with tests",
             "priority": "high", "task_type": task_types[4], "team": teams[0], "assignees": [workers[2], workers[5]],
             "days": 6},
            {"name": "Setup Redis caching", "description": "Add Redis cache for frequently accessed data",
             "priority": "medium", "task_type": task_types[1], "team": teams[0], "assignees": [workers[0]], "days": -3,
             "completed": True},
            {"name": "Migrate to PostgreSQL", "description": "Switch from SQLite to PostgreSQL in production",
             "priority": "urgent", "task_type": task_types[5], "team": teams[0], "assignees": [workers[4], workers[0]],
             "days": -1},

            # Frontend Team tasks
            {"name": "Redesign dashboard UI", "description": "Update dashboard with new design system",
             "priority": "high", "task_type": task_types[1], "team": teams[1], "assignees": [workers[1]], "days": 5},
            {"name": "Fix mobile responsive layout", "description": "Task list breaks on mobile screens",
             "priority": "urgent", "task_type": task_types[0], "team": teams[1], "assignees": [workers[1]], "days": 1},
            {"name": "Implement dark mode", "description": "Add dark/light theme toggle", "priority": "low",
             "task_type": task_types[1], "team": teams[1], "assignees": [workers[1], workers[3]], "days": 20},
            {"name": "Add loading skeletons", "description": "Replace spinners with skeleton loaders",
             "priority": "medium", "task_type": task_types[2], "team": teams[1], "assignees": [workers[1]], "days": 8},
            {"name": "Write component tests", "description": "Add tests for all UI components", "priority": "medium",
             "task_type": task_types[4], "team": teams[1], "assignees": [workers[2], workers[1]], "days": 12},
            {"name": "Update task form validation", "description": "Add client-side validation to task form",
             "priority": "high", "task_type": task_types[0], "team": teams[1], "assignees": [workers[1]], "days": -2},

            # Infrastructure Team tasks
            {"name": "Setup CI/CD pipeline", "description": "Configure GitHub Actions for automated deployment",
             "priority": "urgent", "task_type": task_types[5], "team": teams[2], "assignees": [workers[4]], "days": 4},
            {"name": "Configure Nginx", "description": "Setup reverse proxy and SSL certificates", "priority": "high",
             "task_type": task_types[5], "team": teams[2], "assignees": [workers[4], workers[0]], "days": 7},
            {"name": "Setup monitoring", "description": "Add Prometheus and Grafana monitoring", "priority": "medium",
             "task_type": task_types[5], "team": teams[2], "assignees": [workers[4]], "days": 15},
            {"name": "Docker containerization", "description": "Containerize all services with Docker",
             "priority": "high", "task_type": task_types[5], "team": teams[2], "assignees": [workers[4], workers[0]],
             "days": -5, "completed": True},
            {"name": "Setup log aggregation", "description": "Configure ELK stack for centralized logging",
             "priority": "low", "task_type": task_types[5], "team": teams[2], "assignees": [workers[4]], "days": 25},

            # Mixed tasks
            {"name": "Sprint planning meeting notes", "description": "Document sprint goals and task breakdown",
             "priority": "medium", "task_type": task_types[3], "team": teams[0],
             "assignees": [workers[3], workers[0], workers[1]], "days": 3},
            {"name": "Performance testing", "description": "Run load tests on production environment",
             "priority": "high", "task_type": task_types[4], "team": teams[2], "assignees": [workers[2], workers[4]],
             "days": 6},
            {"name": "Fix login page bug on Safari", "description": "Login button not responding on Safari browser",
             "priority": "urgent", "task_type": task_types[0], "team": teams[1], "assignees": [workers[1]], "days": -1},
            {"name": "Add email notifications",
             "description": "Send email when task is assigned or deadline approaching", "priority": "medium",
             "task_type": task_types[1], "team": teams[0], "assignees": [workers[0], workers[5]], "days": 18},
            {"name": "Code review guidelines", "description": "Write documentation for code review process",
             "priority": "low", "task_type": task_types[3], "team": teams[0], "assignees": [workers[3]], "days": 30},
            {"name": "Security audit", "description": "Review codebase for security vulnerabilities",
             "priority": "urgent", "task_type": task_types[4], "team": teams[2], "assignees": [workers[4], workers[2]],
             "days": 5},
            {"name": "Update dependencies", "description": "Update all npm and pip packages to latest versions",
             "priority": "low", "task_type": task_types[2], "team": teams[0], "assignees": [workers[0]], "days": -7,
             "completed": True},
            {"name": "API rate limiting", "description": "Implement rate limiting for public API endpoints",
             "priority": "high", "task_type": task_types[1], "team": teams[0], "assignees": [workers[0], workers[5]],
             "days": 9},
            {"name": "Backup strategy", "description": "Setup automated database backups", "priority": "high",
             "task_type": task_types[5], "team": teams[2], "assignees": [workers[4]], "days": 11},
            {"name": "Onboarding documentation", "description": "Write guide for new team members", "priority": "low",
             "task_type": task_types[3], "team": teams[1], "assignees": [workers[3]], "days": 35},
        ]

        for data in tasks_data:
            task, created = Task.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "priority": data["priority"],
                    "task_type": data["task_type"],
                    "team": data["team"],
                    "deadline": date.today() + timedelta(days=data["days"]),
                    "is_completed": data.get("completed", False),
                }
            )
            if created:
                task.assignees.set(data["assignees"])

        self.stdout.write("✓ Tasks created")
        self.stdout.write(self.style.SUCCESS("\n✅ Database seeded successfully!"))
        self.stdout.write("\nTest accounts (password: password123):")
        for w in workers_data:
            self.stdout.write(f"  {w['username']} — {w['position'].name}")
