# Пакет с API роутерами для системы бронирования.

from .employees import router as employees_router
from .resources import router as resources_router
from .bookings import router as bookings_router

__all__ = ["employees_router", "resources_router", "bookings_router"]