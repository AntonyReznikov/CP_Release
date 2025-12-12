# API роутер для работы с сотрудниками.
# Содержит эндпоинты для CRUD операций над сотрудниками.


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import models
from backend import schemas
from backend import crud


# Описание
router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    responses={404: {"description": "Сотрудник не найден"}}
)

# Эндпоинт создания нового сотрудника
@router.post(
    "/",
    response_model=schemas.Employee,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового сотрудника",
    description="Создает нового сотрудника в системе. Email должен быть уникальным."
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        employee: Данные нового сотрудника (имя и email)
    Результаты:
        Созданный объект сотрудника с ID
    Исключения:
        HTTPException 400: Если email уже зарегистрирован
    """
    # Проверка уникальности email
    db_employee = crud.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_employee(db=db, employee=employee)

# Эндпоинт получения всех сотрудников
@router.get(
    "/",
    response_model=List[schemas.Employee],
    summary="Получить список всех сотрудников",
    description="Возвращает список всех сотрудников с возможностью пагинации."
)
def read_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        skip: Количество записей для пропуска (для пагинации)
        limit: Максимальное количество записей для возврата
    Результаты:
        Список сотрудников
    """
    # Получение списка сотрудников
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees

# Эндпоинт получения сотрудника по ID
@router.get(
    "/{employee_id}",
    response_model=schemas.Employee,
    summary="Получить сотрудника по ID",
    description="Возвращает информацию о конкретном сотруднике по его ID."
)
def read_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        employee_id: ID сотрудника
    Результаты:
        Данные сотрудника
    Исключения:
        HTTPException 404: Если сотрудник не найден
    """
    # Получение сотрудника
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return db_employee

# Эндпоинт обновления данных сотрудника
@router.put(
    "/{employee_id}",
    response_model=schemas.Employee,
    summary="Обновить данные сотрудника",
    description="Обновляет информацию о сотруднике (имя и/или email)."
)
def update_employee(
    employee_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        employee_id: ID сотрудника
        employee: Новые данные сотрудника
    Результаты:
        Обновленный объект сотрудника
    Исклюячения:
        HTTPException 404: Если сотрудник не найден
        HTTPException 400: Если новый email уже занят
    """
    # Если обновляется email, проверяем уникальность
    if employee.email:
        existing = crud.get_employee_by_email(db, email=employee.email)
        if existing and existing.id != employee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    db_employee = crud.update_employee(db, employee_id=employee_id, employee=employee)
    # Если сотрудние не найден
    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return db_employee

# Эндпоинт удаления сотрудника
@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить сотрудника",
    description="Удаляет сотрудника из системы."
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        employee_id: ID сотрудника
    Исключения:
        HTTPException 404: Если сотрудник не найден
        HTTPException 400: Если у сотрудника есть связанные бронирования
    """
    # Попытка удалить сотрудника
    success = crud.delete_employee(db, employee_id=employee_id)
    # Если не найден пользователь
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return None
