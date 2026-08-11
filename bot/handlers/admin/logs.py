from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.database.repositories import AdminLogRepository
from bot.keyboards.admin import get_back_to_admin_kb

router = Router()

@router.callback_query(F.data == "admin:logs")
async def admin_logs(callback: CallbackQuery, log_repo: AdminLogRepository):
    logs = await log_repo.get_recent(limit=20)
    
    if not logs:
        await callback.message.edit_text(
            "📜 ЛОГИ\n\n"
            "Логи пусты.",
            reply_markup=get_back_to_admin_kb()
        )
        await callback.answer()
        return
    
    logs_text = "📜 АДМИНИСТРАТИВНЫЕ ЛОГИ\n\n"
    
    action_names = {
        'block_user': '🚫 Блокировка',
        'unblock_user': '✅ Разблокировка',
        'add_admin': '➕ Назначение админа',
        'remove_admin': '➖ Снятие админа'
    }
    
    for log in logs:
        action_name = action_names.get(log.action, log.action)
        logs_text += f"{action_name}\n"
        logs_text += f"   Админ: {log.admin_id}\n"
        
        if log.target_user_id:
            logs_text += f"   Цель: {log.target_user_id}\n"
        
        if log.details:
            if 'reason' in log.details:
                logs_text += f"   Причина: {log.details['reason']}\n"
        
        logs_text += f"   {log.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
    
    await callback.message.edit_text(logs_text, reply_markup=get_back_to_admin_kb())
    await callback.answer()
