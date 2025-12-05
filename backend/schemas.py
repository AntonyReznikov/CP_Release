# Модуль с Pydantic схемами для валидации данных API
# Определяет структуру входных и выходных данных для эндпоинтов


from pydantic import BaseModel, EmailStr, Field
from datetime import date as DateType, time as TimeType
from typing import Optional


# Схемы работников
class EmployeeBase(BaseModel):
    # Базовая схема сотрудника с общими атрибутами
    full_name: str = Field(..., min_length=1, max_length=100, description="Полное имя сотрудника")
    email: EmailStr = Field(..., description="Электронная почта сотрудника")


class EmployeeCreate(EmployeeBase):
    # Схема для создания нового сотрудника
    pass


class EmployeeUpdate(BaseModel):
    # Схема для обновления данных сотрудника
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class Employee(EmployeeBase):
    # Схема сотрудника для ответа API
    id: int

    class Config:
        from_attributes = True


# Схемы ресурсов
class ResourceBase(BaseModel):
    # Базовая схема ресурса с общими атрибутами
    name: str = Field(..., min_length=1, max_length=100, description="Название ресурса")
    type: str = Field(..., min_length=1, max_length=50, description="Тип ресурса (комната, проектор и т.д.)")
    capacity: Optional[int] = Field(None, ge=0, description="Вместимость ресурса")


class ResourceCreate(ResourceBase):
    # Схема для создания нового ресурса
    pass


class ResourceUpdate(BaseModel):
    # Схема для обновления данных ресурса
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    capacity: Optional[int] = Field(None, ge=0)


class Resource(ResourceBase):
    # Схема ресурса для ответа API
    id: int

    class Config:
        from_attributes = True


# Схемы бронирований
class BookingBase(BaseModel):
    # Базовая схема бронирования с общими атрибутами
    resource_id: int = Field(..., gt=0, description="ID ресурса")
    employee_id: int = Field(..., gt=0, description="ID сотрудника")
    date: DateType = Field(..., description="Дата бронирования")
    start_time: TimeType = Field(..., description="Время начала бронирования")
    end_time: TimeType = Field(..., description="Время окончания бронирования")


class BookingCreate(BookingBase):
    # Схема для создания нового бронирования
    pass


class BookingUpdate(BaseModel):
    # Схема для обновления данных бронирования
    resource_id: Optional[int] = Field(None, gt=0)
    employee_id: Optional[int] = Field(None, gt=0)
    date: Optional[DateType] = None
    start_time: Optional[TimeType] = None
    end_time: Optional[TimeType] = None


class Booking(BookingBase):
    # Схема бронирования для ответа API
    id: int

    class Config:
        from_attributes = True


class BookingDetail(Booking):
    # Схема бронирования с деталями ресурса и сотрудника
    resource: Resource
    employee: Employee

    class Config:
        from_attributes = True


# Схема отчета
class ResourceUsageReport(BaseModel):
    # Схема для отчета по использованию ресурсов
    resource_id: int = Field(..., description="ID ресурса")
    resource_name: str = Field(..., description="Название ресурса")
    total_hours: float = Field(..., ge=0, description="Общее количество забронированных часов")

    class Config:
        from_attributes = True
