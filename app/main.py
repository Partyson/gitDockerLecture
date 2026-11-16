import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Task
from app.schemas import TaskCreate, TaskRead, TaskUpdate

# Версию прокидываем при сборке образа (см. Dockerfile и CI) —
# удобно на лекции показать, что на сервере выкатился новый коммит.
APP_VERSION = os.getenv("APP_VERSION", "dev")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Для учебного проекта создаём таблицы при старте.
    # В реальном проекте для этого используют миграции (Alembic).
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Tasks API", version=APP_VERSION, lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Hello from Tasks API!", "version": APP_VERSION}


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}


@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(done: bool | None = None, db: Session = Depends(get_db)):
    query = select(Task).order_by(Task.id)
    if done is not None:
        query = query.where(Task.done == done)
    return db.scalars(query).all()


@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task_or_404(task_id: int, db: Session) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return get_task_or_404(task_id, db)


@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = get_task_or_404(task_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_or_404(task_id, db)
    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
