from aiogram import Router
from . import start, bet, profile, history

router = Router()

router.include_router(start.router)
router.include_router(bet.router)
router.include_router(profile.router)
router.include_router(history.router)
