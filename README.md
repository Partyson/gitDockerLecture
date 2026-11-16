# Tasks API — демо для лекции про Git + Docker

Простое REST API на FastAPI + PostgreSQL.

## Запуск

```bash
docker compose up -d --build
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

Остановить: `docker compose down` (с удалением данных БД: `docker compose down -v`).

## Эндпоинты

| Метод  | Путь              | Что делает                         |
|--------|-------------------|------------------------------------|
| GET    | `/`               | Приветствие и версия приложения    |
| GET    | `/health`         | Проверка, что API и БД живы        |
| GET    | `/tasks`          | Список задач (`?done=true/false`)  |
| POST   | `/tasks`          | Создать задачу                     |
| GET    | `/tasks/{id}`     | Получить задачу                    |
| PATCH  | `/tasks/{id}`     | Частично обновить задачу           |
| DELETE | `/tasks/{id}`     | Удалить задачу                     |

Пример:

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Подготовить лекцию"}'
```

## CI/CD

`.github/workflows/docker-publish.yml` на каждый push в `main` собирает образ
и пушит его в GitHub Container Registry с тегами `latest` и `<short-sha>`:

```
ghcr.io/<owner>/<repo>:latest
ghcr.io/<owner>/<repo>:<short-sha>
```
