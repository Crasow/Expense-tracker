# Expense Tracker

Приложение для отслеживания расходов и доходов.

## Быстрый старт

### Автоматическая инициализация (рекомендуется)

Приложение автоматически создаст базу данных и таблицы при первом запуске:

```bash
poetry run uvicorn expense_tracker.main:app --reload
```

### Применение миграций Alembic

Для применения миграций Alembic используйте:

```bash
alembic upgrade head
```

Для создания новой миграции Alembic используйте:

```bash
alembic revision --autogenerate -m "описание миграции"
```

## Требования

- PostgreSQL сервер должен быть запущен
- В файле `.env` должна быть настроена переменная `DATABASE_URL`

Пример переменной в `.env` :
```
DATABASE_URL=postgresql+asyncpg://some_username:password1111@localhost:5432/expense_db
```
