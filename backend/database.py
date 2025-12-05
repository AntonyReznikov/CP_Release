# Модуль настройки базы данных SQLite и SQLAlchemy.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL подключения к SQLite базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./booking_system.db"

# Подключение к базе
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Соединение с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# База для ORM моделей
Base = declarative_base()

# Генератор для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
