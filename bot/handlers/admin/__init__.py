from aiogram import Router
from . import panel, users, admins_management, stats, logs

router = Router()

router.include_router(panel.router)
router.include_router(users.router)
router.include_router(admins_management.router)
router.include_router(stats.router)
router.include_router(logs.router)
