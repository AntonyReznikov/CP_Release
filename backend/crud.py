# Модуль CRUD операций для работы с базой данных
# Содержит функции для создания, чтения, обновления и удаления записей

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import date, datetime, timedelta
from typing import List, Optional
from backend import models
from backend import schemas



# Блок работников 
# Получение сотрудника по ID
def get_employee(db: Session, employee_id: int) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

# Получение сотрудника по email
def get_employee_by_email(db: Session, email: str) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.email == email).first()

# Получение списка всех сотрудников порционно
def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[models.Employee]:
    return db.query(models.Employee).offset(skip).limit(limit).all()

# Создание нового сотрудника
def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    # Создание работника
    db_employee = models.Employee(
        full_name=employee.full_name,
        email=employee.email
    )

    # Внесение изменений в БД
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Обновление данных сотрудника
def update_employee(db: Session, employee_id: int, employee: schemas.EmployeeUpdate) -> Optional[models.Employee]:
    # Получение сотрудника
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None
    
    # Обновление данных полученного сотрудника
    update_data = employee.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)

    # Внесение изменений в БД
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Удаление сотрудника
def delete_employee(db: Session, employee_id: int) -> bool:
    # Возвращает false если сотрудник не найден или имеет связанные бронирования.
    
    # Получение работника
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return False

    # Внесение изменений в БД
    db.delete(db_employee)
    db.commit()

    return True


# Блок ресурсов 
# Получение ресурса по ID
def get_resource(db: Session, resource_id: int) -> Optional[models.Resource]:
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

# Получение списка всех ресурсов порционно
def get_resources(db: Session, skip: int = 0, limit: int = 100) -> List[models.Resource]:
    return db.query(models.Resource).offset(skip).limit(limit).all()

# Создние нового ресурса
def create_resource(db: Session, resource: schemas.ResourceCreate) -> models.Resource:
    # Создание ресурса
    db_resource = models.Resource(
        name=resource.name,
        type=resource.type,
        capacity=resource.capacity
    )
    # Внесение изменений в БД
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

# Обновление данных о ресурсе
def update_resource(db: Session, resource_id: int, resource: schemas.ResourceUpdate) -> Optional[models.Resource]:
    # Получение ресурса
    db_resource = get_resource(db, resource_id)
    if not db_resource:
        return None

    # Внесение изменений ресурса
    update_data = resource.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_resource, key, value)

    # Внесение изменений в БД
    db.commit()
    db.refresh(db_resource)
    return db_resource

# Удаление ресурса
def delete_resource(db: Session, resource_id: int) -> bool:
    # Возвращает false если ресурс не найден или имеет связанные бронирования.
    
    # Получение ресурса
    db_resource = get_resource(db, resource_id)
    if not db_resource:
        return False

    # Внесение изменений в БД
    db.delete(db_resource)
    db.commit()
    return True


# Блок бронирований

# Получение бронирование по ID
def get_booking(db: Session, booking_id: int) -> Optional[models.Booking]:
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

# Получение списка всех бронирований порционно
def get_bookings(db: Session, skip: int = 0, limit: int = 100) -> List[models.Booking]:
    return db.query(models.Booking).offset(skip).limit(limit).all()

# Проверка, есть ли конфликтующие бронирования для данного ресурса
def check_booking_conflict(
    db: Session,
    resource_id: int,
    booking_date: date,
    start_time: datetime.time,
    end_time: datetime.time,
    exclude_booking_id: Optional[int] = None
) -> bool:
    """
    Аргументы:
        db: Сессия базы данных
        resource_id: ID ресурса
        booking_date: Дата бронирования
        start_time: Время начала
        end_time: Время окончания
        exclude_booking_id: ID бронирования для исключения из проверки (при обновлении)

    Результаты:
        true - есть конфликт
        false - нет конфликта
    """

    # Проверка пересечения временных интервалов
    query = db.query(models.Booking).filter(
        and_(
            models.Booking.resource_id == resource_id,
            models.Booking.date == booking_date,
            models.Booking.start_time < end_time,
            models.Booking.end_time > start_time
        )
    )

    # Исключение текущего бронирования при обновлении
    if exclude_booking_id:
        query = query.filter(models.Booking.id != exclude_booking_id)

    return query.first() is not None

# Создание нового бронирования
def create_booking(db: Session, booking: schemas.BookingCreate) -> models.Booking:
    # Создание бронирования
    db_booking = models.Booking(
        resource_id=booking.resource_id,
        employee_id=booking.employee_id,
        date=booking.date,
        start_time=booking.start_time,
        end_time=booking.end_time
    )

    # Внесение изменений в БД
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

# Обновление бронирования
def update_booking(db: Session, booking_id: int, booking: schemas.BookingUpdate) -> Optional[models.Booking]:
    # Получение бронирования
    db_booking = get_booking(db, booking_id)
    if not db_booking:
        return None

    # Внесение изменений в бронирование
    update_data = booking.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_booking, key, value)

    # Внесение изменений в БД
    db.commit()
    db.refresh(db_booking)
    return db_booking

# Удаление бронирования
def delete_booking(db: Session, booking_id: int) -> bool:
    # Получение бронирования
    db_booking = get_booking(db, booking_id)
    if not db_booking:
        return False

    # Внесение изменений в БД
    db.delete(db_booking)
    db.commit()
    return True


# Блок дополнительных запросов 
# Получение всех бронирований на сегодня
def get_bookings_today(db: Session) -> List[models.Booking]:
    today = date.today()
    return db.query(models.Booking).filter(models.Booking.date == today).all()

# Получение всех бронирований для конкретного:
# - ресурса
def get_bookings_by_resource(db: Session, resource_id: int) -> List[models.Booking]:
    return db.query(models.Booking).filter(models.Booking.resource_id == resource_id).all()

# - сотрудника
def get_bookings_by_employee(db: Session, employee_id: int) -> List[models.Booking]:
    return db.query(models.Booking).filter(models.Booking.employee_id == employee_id).all()

# Получение отчета по загрузке ресурсов за прошедший месяц месяц, с момента запроса
def get_resource_usage_report(db: Session) -> List[dict]:

    one_month_ago = date.today() - timedelta(days=30)

    # Получение всех ресурсов
    resources = db.query(models.Resource).all()

    # Формирование отчета
    report = []
    for resource in resources:
        # Получение всех бронирований для этого ресурса за прошедший месяц месяц, с момента запроса
        bookings = db.query(models.Booking).filter(
            and_(
                models.Booking.resource_id == resource.id,
                models.Booking.date >= one_month_ago
            )
        ).all()

        # Вычисление общего времени
        total_hours = 0.0
        for booking in bookings:
            # Преобразование time в datetime для вычисления разницы
            start = datetime.combine(date.today(), booking.start_time)
            end = datetime.combine(date.today(), booking.end_time)
            duration = (end - start).total_seconds() / 3600  # Перевод в часы
            total_hours += duration

        # Добавление в отчет только ресурсов с бронированиями
        if total_hours > 0:
            report.append({
                'resource_id': resource.id,
                'resource_name': resource.name,
                'total_hours': round(total_hours, 2)
            })

    # Сортировка по убыванию
    report.sort(key=lambda x: x['total_hours'], reverse=True)

    return report
