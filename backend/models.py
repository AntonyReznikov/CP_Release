# Модуль с моделями базы данных.
# Описание структуры таблиц: Employee, Resource, Booking.

from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

# Модель сотрудников
class Employee(Base):
    """
    Атрибуты:
        id: Уникальный идентификатор сотрудника
        full_name: Полное имя сотрудника
        email: Электронная почта сотрудника
        bookings: Связь с бронированиями сотрудника
    """
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)

    # Связь один-ко-многим с бронированиями
    bookings = relationship("Booking", back_populates="employee", cascade="all, delete-orphan")

# Модель ресурсов
class Resource(Base):
    """
    Атрибуты:
        id: Уникальный идентификатор ресурса
        name: Название ресурса ("Переговорная №1" и др.)
        type: Тип ресурса ("комната", "проектор")
        capacity: Вместимость (для комнат) или другие характеристики
        bookings: Связь с бронированиями ресурса
    """
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False, index=True)
    capacity = Column(Integer, nullable=True)

    # Связь один-ко-многим с бронированиями
    bookings = relationship("Booking", back_populates="resource", cascade="all, delete-orphan")

# Модель бронирований
class Booking(Base):
    """
    Атрибуты:
        id: Уникальный идентификатор бронирования
        resource_id: ID забронированного ресурса
        employee_id: ID сотрудника, создавшего бронирование
        date: Дата бронирования
        start_time: Время начала бронирования
        end_time: Время окончания бронирования
        resource: Связь с объектом ресурса
        employee: Связь с объектом сотрудника
    """
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    # Связи с другими таблицами
    resource = relationship("Resource", back_populates="bookings")
    employee = relationship("Employee", back_populates="bookings")
