from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from bot.filters.admin import IsAdmin, IsPrivateChat
from bot.keyboards.admin import get_admin_main_kb

router = Router()

@router.message(Command("adm"), IsAdmin(), IsPrivateChat())
async def cmd_admin(message: Message):
    await message.answer(
        "🛡️ АДМИНИСТРАТИВНАЯ ПАНЕЛЬ\n\n"
        "Выберите раздел:",
        reply_markup=get_admin_main_kb()
    )

@router.message(Command("adm"))
async def cmd_admin_denied(message: Message):
    await message.answer("❌ Доступ запрещён.")

@router.callback_query(F.data == "admin:back")
async def admin_back(callback: CallbackQuery):
    await callback.message.edit_text(
        "🛡️ АДМИНИСТРАТИВНАЯ ПАНЕЛЬ\n\n"
        "Выберите раздел:",
        reply_markup=get_admin_main_kb()
    )
    await callback.answer()
