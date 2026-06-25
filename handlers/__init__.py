from aiogram import Router

from .start import router as start_router
from .calculator import router as calculator_router


def get_all_routers() -> list[Router]:
    """Return routers in priority order: start first, then calculator."""
    return [start_router, calculator_router]
