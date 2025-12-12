FROM python:3.11-slim

WORKDIR /app

# Копирование зависимости и их установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Команда запуска
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]