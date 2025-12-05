# API роутер для работы с ресурсами.
# Содержит эндпоинты для CRUD операций над ресурсами (комнатами, оборудованием).


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import schemas
import crud

# Описание
router = APIRouter(
    prefix="/resources",
    tags=["Resources"],
    responses={404: {"description": "Ресурс не найден"}}
)

# Эндпоинт создания нового ресурса
@router.post(
    "/",
    response_model=schemas.Resource,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый ресурс",
    description="Создает новый ресурс в системе (переговорную комнату, проектор и т.д.)."
)
def create_resource(
    resource: schemas.ResourceCreate,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        resource: Данные нового ресурса (название, тип, вместимость)
    Результаты:
        Созданный объект ресурса с ID
    """
    # Создание ресурса
    return crud.create_resource(db=db, resource=resource)

# Эндпоинт получения всех ресурсов
@router.get(
    "/",
    response_model=List[schemas.Resource],
    summary="Получить список всех ресурсов",
    description="Возвращает список всех доступных ресурсов с возможностью пагинации."
)
def read_resources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        skip: Количество записей для пропуска (для пагинации)
        limit: Максимальное количество записей для возврата
    Результаты:
        Список ресурсов
    """
    # Получить ресурс
    resources = crud.get_resources(db, skip=skip, limit=limit)
    return resources

# Эндпоинт получения ресурса по ID
@router.get(
    "/{resource_id}",
    response_model=schemas.Resource,
    summary="Получить ресурс по ID",
    description="Возвращает информацию о конкретном ресурсе по его ID."
)
def read_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        resource_id: ID ресурса
    Результаты:
        Данные ресурса
    Исключения:
        HTTPException 404: Если ресурс не найден
    """
    # Получить ресурс по ID
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    return db_resource

# Эндпоинт обновления ресурса
@router.put(
    "/{resource_id}",
    response_model=schemas.Resource,
    summary="Обновить данные ресурса",
    description="Обновляет информацию о ресурсе (название, тип, вместимость)."
)
def update_resource(
    resource_id: int,
    resource: schemas.ResourceUpdate,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        resource_id: ID ресурса
        resource: Новые данные ресурса
    Результаты:
        Обновленный объект ресурса
    Исключения:
        HTTPException 404: Если ресурс не найден
    """
    # Обновление ресурса
    db_resource = crud.update_resource(db, resource_id=resource_id, resource=resource)
    if db_resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    return db_resource

# Эндпоинт удаления ресурса
@router.delete(
    "/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить ресурс",
    description="Удаляет ресурс из системы."
)
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    """
    Аргументы:
        resource_id: ID ресурса
    Исключения:
        HTTPException 404: Если ресурс не найден
        HTTPException 400: Если у ресурса есть связанные бронирования
    """
    # Попытка удалить ресурс
    try:
        success = crud.delete_resource(db, resource_id=resource_id)
        # Если безуспешно
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
    return None
