__all__ = ("router",)

from aiogram import Router

from .folder_router import router as folder_router
from .base_router import router as base_router
from .upload_router import router as upload_router
from .recognize_images_router import router as handle_photo_router
from .registration_router import router as registration_router

router = Router(name=__name__)

router.include_routers(
    folder_router,
    base_router,
    upload_router,
    handle_photo_router,
    registration_router
)
