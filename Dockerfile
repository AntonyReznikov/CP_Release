# Используем официальный Python
FROM python:3.11-slim

# Устанавливаем рабочую папку
WORKDIR /app

# Копируем зависимости
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь бекенд и фронтенд
COPY backend ./backend
COPY frontend ./frontend

# Создаём папку для БД
RUN mkdir -p /data

# Открываем порт
EXPOSE 8000

# Запуск: FastAPI + обслуживание статики
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]