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

# Настройка CORS для разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(employees.router)
app.include_router(resources.router)
app.include_router(bookings.router)

# Путь к фронтенду
FRONTEND_PATH = "/app/frontend"

# Подключение статических файлов
if os.path.exists(FRONTEND_PATH):
    # Статические файлы фронтенда
    app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")
    
    # Главная страница
    @app.get("/")
    async def serve_index():
        index_file = os.path.join(FRONTEND_PATH, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "Frontend files not found"}
    
    # Обработка всех путей для SPA
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        #  Поиск статического файла
        file_path = os.path.join(FRONTEND_PATH, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        
        # Если файл не найден
        index_file = os.path.join(FRONTEND_PATH, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        
        return {"message": "File not found"}
else:
    @app.get("/")
    def root():
        return {"message": "Backend is running", "docs": "/docs", "status": "Frontend not found"}

# Эндпоинт health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Эндпоинт для проверки доступности API
@app.get("/api/status")
def api_status():
    return {"status": "running", "version": "1.0.0"}