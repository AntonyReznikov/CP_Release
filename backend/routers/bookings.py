# API роутер для работы с бронированиями.
# Содержит эндпоинты для CRUD операций, фильтрации и отчетов.


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import schemas
import crud

# Описание
router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
    responses={404: {"description": "Бронирование не найдено"}}
)

# Эндпоинт создания нового бронирования
@router.post(
    "/",
    response_model=schemas.Booking,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новое бронирование",
    description="Создает новое бронирование с проверкой на пересечение с существующими бронированиями."
)
def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        booking: Данные нового бронирования
    Результаты:
        Созданный объект бронирования с ID
    Исключения:
        HTTPException 400: Если время окончания раньше времени начала
        HTTPException 404: Если ресурс или сотрудник не найдены
        HTTPException 409: Если ресурс уже занят в это время
    """
    # Валидация времени
    if booking.end_time <= booking.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time"
        )

    # Проверка существования ресурса
    db_resource = crud.get_resource(db, resource_id=booking.resource_id)
    if not db_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )

    # Проверка существования сотрудника
    db_employee = crud.get_employee(db, employee_id=booking.employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    # Проверка на пересечение бронирований
    if crud.check_booking_conflict(
        db,
        resource_id=booking.resource_id,
        booking_date=booking.date,
        start_time=booking.start_time,
        end_time=booking.end_time
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Resource is already booked for this time slot"
        )

    return crud.create_booking(db=db, booking=booking)

# Эндпоинт получения списка всех бронирований
@router.get(
    "/",
    response_model=List[schemas.BookingDetail],
    summary="Получить список всех бронирований",
    description="Возвращает список всех бронирований с информацией о ресурсах и сотрудниках."
)
def read_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        skip: Количество записей для пропуска (для пагинации)
        limit: Максимальное количество записей для возврата
    Результаты:
        Список бронирований с детальной информацией
    """
    # Получения списка бронирований
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings

# Эндпоинт получения бронирования на сегодня
@router.get(
    "/today",
    response_model=List[schemas.BookingDetail],
    summary="Получить бронирования на сегодня",
    description="Возвращает все бронирования на сегодняшнюю дату."
)
def read_bookings_today(db: Session = Depends(get_db)):
    """
    Результаты:
        Список бронирований на сегодня
    """
    bookings = crud.get_bookings_today(db)
    return bookings

# Эндпоинт получения бронирований по ресурсу
@router.get(
    "/by_resource/{resource_id}",
    response_model=List[schemas.BookingDetail],
    summary="Получить бронирования по ресурсу",
    description="Возвращает все бронирования для конкретного ресурса (расписание комнаты)."
)
def read_bookings_by_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        resource_id: ID ресурса
    Результаты:
        Список бронирований для ресурса
    Исключения:
        HTTPException 404: Если ресурс не найден
    """
    # Проверка существования ресурса
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )

    bookings = crud.get_bookings_by_resource(db, resource_id=resource_id)
    return bookings

# Эндпоинт получения бронирования по сотруднику
@router.get(
    "/by_employee/{employee_id}",
    response_model=List[schemas.BookingDetail],
    summary="Получить бронирования по сотруднику",
    description="Возвращает все бронирования конкретного сотрудника ('мои бронирования')."
)
def read_bookings_by_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        employee_id: ID сотрудника
    Результаты:
        Список бронирований сотрудника
    Исключения:
        HTTPException 404: Если сотрудник не найден
    """
    # Проверка существования сотрудника
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    bookings = crud.get_bookings_by_employee(db, employee_id=employee_id)
    return bookings

# Эндпоинт получения бронирования по ID
@router.get(
    "/{booking_id}",
    response_model=schemas.BookingDetail,
    summary="Получить бронирование по ID",
    description="Возвращает информацию о конкретном бронировании по его ID."
)
def read_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        booking_id: ID бронирования
    Результаты:
        Данные бронирования
    Исключения:
        HTTPException 404: Если бронирование не найдено
    """
    # Проверка существования бронироания
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return db_booking

# Эндпоинт обновления бронирования
@router.put(
    "/{booking_id}",
    response_model=schemas.Booking,
    summary="Обновить бронирование",
    description="Обновляет бронирование с проверкой на пересечения."
)
def update_booking(
    booking_id: int,
    booking: schemas.BookingUpdate,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        booking_id: ID бронирования
        booking: Новые данные бронирования
    Результаты:
        Обновленный объект бронирования
    Исключения:
        HTTPException 404: Если бронирование не найдено
        HTTPException 400: Если время окончания раньше времени начала
        HTTPException 409: Если новое время конфликтует с другими бронированиями
    """
    # Получаем существующее бронирование
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if not db_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Определяем финальные значения для проверки
    resource_id = booking.resource_id if booking.resource_id is not None else db_booking.resource_id
    booking_date = booking.date if booking.date is not None else db_booking.date
    start_time = booking.start_time if booking.start_time is not None else db_booking.start_time
    end_time = booking.end_time if booking.end_time is not None else db_booking.end_time

    # Валидация времени
    if end_time <= start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time"
        )

    # Проверка на пересечение с другими бронированиями (исключая текущее)
    if crud.check_booking_conflict(
        db,
        resource_id=resource_id,
        booking_date=booking_date,
        start_time=start_time,
        end_time=end_time,
        exclude_booking_id=booking_id
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Resource is already booked for this time slot"
        )

    db_booking = crud.update_booking(db, booking_id=booking_id, booking=booking)
    return db_booking

# Эндпоинт удаления бронирования
@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить бронирование",
    description="Удаляет бронирование из системы."
)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        booking_id: ID бронирования
    Исключения:
        HTTPException 404: Если бронирование не найдено
    """
    # Проверка успешности удаления
    success = crud.delete_booking(db, booking_id=booking_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return None


# Отчеты
# Эндпоинт отчета по загрузке ресурсов
@router.get(
    "/report/resource_usage",
    response_model=List[schemas.ResourceUsageReport],
    tags=["Reports"],
    summary="Отчет по загрузке ресурсов",
    description="Возвращает суммарное количество часов бронирования каждого ресурса за последний месяц."
)
def get_resource_usage_report(db: Session = Depends(get_db)):
    """
    Результаты:
        Список с информацией о ресурсах и суммарных часах бронирования
    """
    # Получить отчет
    report = crud.get_resource_usage_report(db)
    return report
