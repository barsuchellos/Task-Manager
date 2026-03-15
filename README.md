# 📋 Task Manager

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

A team-oriented task management web application built with Django. Users can manage tasks, track progress, and collaborate within teams — with access control based on team membership.

## 🚀 Live Demo
👉 [https://task-manager-7xbn.onrender.com/](https://task-manager-7xbn.onrender.com/)
> 🔑 **Test credentials:** `john_dev` / `SunnyDay23`

---

## 📸 Screenshots

![Dashboard](https://github.com/user-attachments/assets/e6aff4f9-7820-413a-8e4d-ace6019f3b53)

![Tasks](https://github.com/user-attachments/assets/3beeb4a4-3a19-417c-b547-4f5c30113a54)

![Team](https://github.com/user-attachments/assets/e551a3c0-168b-4ab1-9f75-190bb61d2e5e)

---

## ✨ Features

- 🔐 **Authentication** — Registration, login/logout, session management
- ✅ **Task CRUD** — Create, update, delete, toggle completion
- 👥 **Team-based Access** — Users see only tasks from their teams or assigned to them
- 🔍 **Filtering** — Filter tasks by name, task type, and assignees
- 📊 **Dashboard** — Overview of total, completed, pending and overdue tasks
- 📄 **Pagination** — 7 tasks per page with filter persistence across pages
- 👤 **Worker Profiles** — View team members, edit own profile with password change

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| Framework | Django 6.0 |
| Database | PostgreSQL |
| Frontend | Tabler UI + Bootstrap 5 |
| Auth | Django built-in authentication |
| Architecture | Services / Selectors pattern |

---

## 🏗 Project Structure

```
task_manager/
├── task_manager/
│   ├── settings/
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
│
├── tasks/
│   ├── management/
│   ├── migrations/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_selectors.py
│   │   ├── test_services.py
│   │   └── test_views.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── selectors.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── includes/
│   ├── registration/
│   ├── tasks/
│   └── base.html
│
├── .env
├── .gitignore
└── requirements/
```

---

## 📐 Architecture — Services / Selectors

```
HTTP Request
     │
     ▼
  ┌──────┐
  │ View │  ← HTTP logic only (request/response/redirect)
  └──┬───┘
     │
     ├──[GET]──────► ┌──────────┐
     │               │ Selector │ ← Read from DB (filter, annotate)
     │               └──────────┘
     │
     └──[POST]─────► ┌─────────┐
                     │ Service │ ← Write to DB (create/update/delete)
                     └────┬────┘
                          │
                          ▼
                      Database
```

**Ground rules:**
- Views **never** access `Model.objects` directly
- Selectors **never** modify data
- Services **never** know about `request`

---

## 📊 Data Models

```
Worker (AbstractUser)        Position
  ├── position ──────────────► (FK)
  └── teams ◄──────────────── Team (M2M via members)

Task
  ├── task_type ─────────────► TaskType (FK)
  ├── team ──────────────────► Team (FK)
  └── assignees ◄──────────── Worker (M2M)
```

---

## ⚙️ Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/barsuchellos/task-manager.git
cd task-manager

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env with your database and secret key

# 5. Apply migrations
python manage.py migrate

# 6. Seed test data (creates 6 workers, 3 teams, 30 tasks)
python manage.py seed_data

# 7. Run development server
python manage.py runserver
```

---

## 🌍 Environment Variables

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/taskmanager
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 🧪 Running Tests

```bash
python manage.py test tasks
```

Test coverage includes:
- **Selectors** — ORM queries, access control, filtering logic
- **Services** — create, update, delete, toggle operations
- **Views** — HTTP status codes, redirects, template responses

---

## 🚀 Deployment

This project is deployed on **Render** with PostgreSQL.

To deploy your own instance:
1. Create a PostgreSQL database on Render
2. Connect your GitHub repository
3. Set environment variables in Render dashboard
4. Deploy — Render runs migrations automatically via build command

---

## 👤 Author

Built as a portfolio project to demonstrate Django backend skills:
ORM, architecture patterns, authentication, testing, and deployment.

[![GitHub](https://img.shields.io/badge/GitHub-barsuchellos-181717?logo=github)](https://github.com/barsuchellos)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Bohdan_Borsuk-0A66C2?logo=linkedin)](https://www.linkedin.com/in/bohdan-borsuk/?locale=uk)
