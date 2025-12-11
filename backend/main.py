# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.database import engine, Base
from backend.routers import employees, resources, bookings
import os

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Приложение
app = FastAPI(
    title="Booking System API",
    description="API для системы бронирования офисных ресурсов",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры API
app.include_router(employees.router, prefix="/employees")
app.include_router(resources.router, prefix="/resources")
app.include_router(bookings.router, prefix="/bookings")

# Путь к фронтенду
FRONTEND_PATH = "/app/frontend"
os.makedirs(FRONTEND_PATH, exist_ok=True)

# Статика
app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")

# SPA: главная страница
@app.get("/")
async def serve_frontend():
    return FileResponse(f"{FRONTEND_PATH}/index.html")

# SPA: fallback для роутинга
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    file_path = f"{FRONTEND_PATH}/{full_path}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(f"{FRONTEND_PATH}/index.html")

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}