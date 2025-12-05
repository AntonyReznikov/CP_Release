# Главный модуль FastAPI приложения
# Настройка и запуск веб-сервера API

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import employees, resources, bookings

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

# Создание приложения
app = FastAPI(
    title="Booking System API",
    description="API для системы бронирования офисных ресурсов (переговорных комнат и оборудования)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS для работы с фронтендом (безопасность)
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

# Корневой эндпоинт 
# Возвращает приветственное сообщение и ссылки на документацию.
@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Booking System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "employees": "/employees",
            "resources": "/resources",
            "bookings": "/bookings",
            "reports": "/bookings/report/resource_usage"
        }
    }


# Эндпоинт получения состояния API
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    # Запуск сервера
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True  # Автоматическая перезагрузка при изменении кода
    )
