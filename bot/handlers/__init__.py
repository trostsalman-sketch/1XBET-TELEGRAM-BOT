from aiogram import Router
from . import user, admin

router = Router()

router.include_router(user.router)
router.include_router(admin.router)
