from typing import Optional, List
from sqlalchemy import select, func, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from .models import User, Admin, Bet, Transaction, AdminLog

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_or_create(self, telegram_id: int, username: Optional[str] = None, 
                           first_name: Optional[str] = None, last_name: Optional[str] = None) -> User:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        
        return user
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def block_user(self, telegram_id: int, reason: str, blocked_by: int):
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            user.is_blocked = True
            user.block_reason = reason
            user.blocked_at = datetime.utcnow()
            user.blocked_by = blocked_by
            await self.session.commit()
    
    async def unblock_user(self, telegram_id: int):
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            user.is_blocked = False
            user.block_reason = None
            user.blocked_at = None
            user.blocked_by = None
            await self.session.commit()
    
    async def get_stats(self, telegram_id: int) -> dict:
        stmt_total = select(func.count(Bet.id)).where(Bet.user_id == telegram_id)
        stmt_wins = select(func.count(Bet.id)).where(and_(Bet.user_id == telegram_id, Bet.status == 'won'))
        stmt_losses = select(func.count(Bet.id)).where(and_(Bet.user_id == telegram_id, Bet.status == 'lost'))
        
        total = (await self.session.execute(stmt_total)).scalar() or 0
        wins = (await self.session.execute(stmt_wins)).scalar() or 0
        losses = (await self.session.execute(stmt_losses)).scalar() or 0
        
        win_rate = (wins / total * 100) if total > 0 else 0
        
        return {
            "total_bets": total,
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 2)
        }
    
    async def count_all(self) -> int:
        stmt = select(func.count(User.id))
        result = await self.session.execute(stmt)
        return result.scalar() or 0

class AdminRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def is_admin(self, telegram_id: int) -> bool:
        stmt = select(Admin).where(Admin.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    async def get_role(self, telegram_id: int) -> Optional[str]:
        stmt = select(Admin.role).where(Admin.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def add_admin(self, telegram_id: int, appointed_by: int):
        admin = Admin(
            telegram_id=telegram_id,
            role='admin',
            appointed_by=appointed_by
        )
        self.session.add(admin)
        await self.session.commit()
    
    async def remove_admin(self, telegram_id: int):
        stmt = select(Admin).where(Admin.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        admin = result.scalar_one_or_none()
        
        if admin and admin.role != 'owner':
            await self.session.delete(admin)
            await self.session.commit()
    
    async def get_all(self) -> List[Admin]:
        stmt = select(Admin).order_by(Admin.appointed_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

class BetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user_id: int, amount: int, game: str, choice: str) -> Bet:
        bet = Bet(
            user_id=user_id,
            amount=amount,
            game=game,
            choice=choice,
            status='pending'
        )
        self.session.add(bet)
        await self.session.commit()
        await self.session.refresh(bet)
        return bet
    
    async def get_by_id(self, bet_id: int) -> Optional[Bet]:
        stmt = select(Bet).where(Bet.id == bet_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def complete_bet(self, bet_id: int, result: str, status: str):
        bet = await self.get_by_id(bet_id)
        if bet and bet.status == 'active':
            bet.result = result
            bet.status = status
            bet.completed_at = datetime.utcnow()
            await self.session.commit()
    
    async def activate_bet(self, bet_id: int, transaction_id: str):
        bet = await self.get_by_id(bet_id)
        if bet and bet.status == 'pending':
            bet.status = 'active'
            bet.transaction_id = transaction_id
            await self.session.commit()
    
    async def get_user_history(self, telegram_id: int, limit: int = 10, offset: int = 0) -> List[Bet]:
        stmt = select(Bet).where(Bet.user_id == telegram_id).order_by(desc(Bet.created_at)).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def count_all(self) -> int:
        stmt = select(func.count(Bet.id))
        result = await self.session.execute(stmt)
        return result.scalar() or 0
    
    async def count_by_status(self, status: str) -> int:
        stmt = select(func.count(Bet.id)).where(Bet.status == status)
        result = await self.session.execute(stmt)
        return result.scalar() or 0
    
    async def get_total_amount(self) -> int:
        stmt = select(func.sum(Bet.amount))
        result = await self.session.execute(stmt)
        return result.scalar() or 0
    
    async def get_game_stats(self) -> dict:
        games = ['basketball', 'football', 'fortune']
        stats = {}
        
        for game in games:
            stmt_total = select(func.count(Bet.id)).where(Bet.game == game)
            stmt_won = select(func.count(Bet.id)).where(and_(Bet.game == game, Bet.status == 'won'))
            
            total = (await self.session.execute(stmt_total)).scalar() or 0
            won = (await self.session.execute(stmt_won)).scalar() or 0
            
            stats[game] = {
                'total': total,
                'won': won,
                'lost': total - won
            }
        
        return stats

class AdminLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def log(self, admin_id: int, action: str, target_user_id: Optional[int] = None, details: Optional[dict] = None):
        log = AdminLog(
            admin_id=admin_id,
            action=action,
            target_user_id=target_user_id,
            details=details
        )
        self.session.add(log)
        await self.session.commit()
    
    async def get_recent(self, limit: int = 50) -> List[AdminLog]:
        stmt = select(AdminLog).order_by(desc(AdminLog.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
