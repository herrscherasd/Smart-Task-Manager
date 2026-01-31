# Smart Task Manager with AI Priority

Smart Task Manager — это минималистичное веб-приложение для управления задачами с автоматическим AI-анализом.
Пользователь добавляет задачу в свободной форме, а система сама определяет приоритет, категорию, примерное время выполнения и подзадачи.

Проект реализован как production-ready MVP с чистой архитектурой, асинхронной БД и Docker-окружением.

---

## 🚀 Features

- Добавление задач в свободной форме (plain text)
- AI-анализ задачи:
  - приоритет (High / Medium / Low)
  - категория (Work, Personal, Learning, Health, Other)
  - оценка времени выполнения
  - генерация подзадач
- Полный CRUD:
  - список задач
  - страница деталей
  - редактирование (с повторным AI-анализом)
  - удаление
- Web UI (FastAPI + Jinja2)
- PostgreSQL + Alembic migrations
- Полностью Dockerized

---

## 🧱 Tech Stack

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy (async)**
- **PostgreSQL**
- **Alembic**
- **Google Gemini API**
- **Jinja2**
- **Docker / docker-compose**

---

## 📁 Project Structure

```text
app/
├── api/            # JSON API endpoints
├── web/            # HTML views (Jinja2)
├── services/       # Business logic (AI + persistence)
├── db/             # DB models and session
├── core/           # Config and clients
├── templates/      # HTML templates
├── static/         # CSS
alembic/            # DB migrations
Dockerfile
docker-compose.yml
```

---

## ⚙️ Environment Variables

Создай файл .env на основе .env.example:
```
# async DB URL (application)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/tasks_db

# sync DB URL (alembic)
DATABASE_URL_SYNC=postgresql+psycopg2://postgres:postgres@db:5432/tasks_db

# Gemini
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

---

## 🐳 Run with Docker
```
docker compose up --build
```

После запуска:

Web UI: http://localhost:8000

Health check: http://localhost:8000/ping

Alembic migrations применяются автоматически при старте контейнера.

---

## 🧪 API Endpoints

```POST /tasks``` — создать задачу

```GET /tasks``` — список задач

```DELETE /tasks/{id}``` — удалить задачу

Web-интерфейс доступен через браузер, API можно использовать отдельно.

---

## 🧠 Architecture Notes

- Web (```web/```) и API (```api/```) слои являются thin adapters

- Вся бизнес-логика вынесена в ```services/```    

- AI-анализ инкапсулирован и легко заменяем

- Alembic использует sync-драйвер, приложение — async

- Docker окружение полностью воспроизводимо