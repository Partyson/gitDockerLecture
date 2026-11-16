FROM python:3.13-slim

# Не создавать .pyc и сразу писать логи в stdout (их видно в docker logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала только зависимости: этот слой кешируется и не пересобирается,
# пока не изменится requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом код — он меняется часто, поэтому идёт последним
COPY app ./app

# Версия приложения (в CI сюда передаётся хеш коммита)
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

# Не запускаем приложение от root
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
