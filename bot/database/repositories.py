from sqlalchemy import select, update, delete, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List

from .models import User, Bet, AdminAction


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, user_id: int, username: Optional[str] = None) -> User:
        user = User(id=user_id, username=username)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_or_create(self, user_id: int, username: Optional[str] = None) -> User:
        user = await self.get_by_id(user_id)
        if not user:
            user = await self.create(user_id, username)
        return user
    
    async def update_balance(self, user_id: int, amount: int) -> bool:
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(balance=User.balance + amount)
        )
        await self.session.commit()
        return True
    
    async def set_balance(self, user_id: int, balance: int) -> bool:
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(balance=balance)
        )
        await self.session.commit()
        return True
    
    async def block_user(self, user_id: int) -> bool:
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_blocked=True)
        )
        await self.session.commit()
        return True
    
    async def unblock_user(self, user_id: int) -> bool:
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_blocked=False)
        )
        await self.session.commit()
        return True
    
    async def set_admin(self, user_id: int, is_admin: bool = True) -> bool:
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_admin=is_admin)
        )
        await self.session.commit()
        return True
    
    async def get_all_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        result = await self.session.execute(
            select(User).limit(limit).offset(offset)
        )
        return list(result.scalars().all())
    
    async def get_blocked_users(self) -> List[User]:
        result = await self.session.execute(
            select(User).where(User.is_blocked == True)
        )
        return list(result.scalars().all())
    
    async def get_admins(self) -> List[User]:
        result = await self.session.execute(
            select(User).where(User.is_admin == True)
        )
        return list(result.scalars().all())
    
    async def count_users(self) -> int:
        result = await self.session.execute(
            select(func.count(User.id))
        )
        return result.scalar_one()
    
    async def count_blocked_users(self) -> int:
        result = await self.session.execute(
            select(func.count(User.id)).where(User.is_blocked == True)
        )
        return result.scalar_one()
    
    async def count_admins(self) -> int:
        result = await self.session.execute(
            select(func.count(User.id)).where(User.is_admin == True)
        )
        return result.scalar_one()


class BetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(
        self,
        user_id: int,
        amount: int,
        game: str,
        choice: str,
        transaction_id: Optional[str] = None
    ) -> Bet:
        bet = Bet(
            user_id=user_id,
            amount=amount,
            game=game,
            choice=choice,
            status="pending",
            transaction_id=transaction_id
        )
        self.session.add(bet)
        await self.session.commit()
        await self.session.refresh(bet)
        return bet
    
    async def get_by_id(self, bet_id: int) -> Optional[Bet]:
        result = await self.session.execute(
            select(Bet).where(Bet.id == bet_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_bets(
        self,
        user_id: int,
        limit: int = 10,
        offset: int = 0
    ) -> List[Bet]:
        result = await self.session.execute(
            select(Bet)
            .where(Bet.user_id == user_id)
            .order_by(desc(Bet.created_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
    
    async def get_by_status(self, status: str, limit: int = 50) -> List[Bet]:
        result = await self.session.execute(
            select(Bet)
            .where(Bet.status == status)
            .order_by(desc(Bet.created_at))
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_pending_bets(self, limit: int = 50) -> List[Bet]:
        return await self.get_by_status("pending", limit)
    
    async def get_active_bets(self, limit: int = 50) -> List[Bet]:
        return await self.get_by_status("active", limit)
    
    async def update_status(
        self,
        bet_id: int,
        status: str,
        result: Optional[str] = None
    ) -> bool:
        values = {"status": status}
        if result:
            values["result"] = result
        if status in ["won", "lost", "rejected"]:
            values["completed_at"] = datetime.utcnow()
        
        await self.session.execute(
            update(Bet)
            .where(Bet.id == bet_id)
            .values(**values)
        )
        await self.session.commit()
        return True
    
    async def delete_bet(self, bet_id: int) -> bool:
        await self.session.execute(
            delete(Bet).where(Bet.id == bet_id)
        )
        await self.session.commit()
        return True
    
    async def count_bets(self) -> int:
        result = await self.session.execute(
            select(func.count(Bet.id))
        )
        return result.scalar_one()
    
    async def count_bets_by_status(self, status: str) -> int:
        result = await self.session.execute(
            select(func.count(Bet.id)).where(Bet.status == status)
        )
        return result.scalar_one()
    
    async def get_total_wagered(self) -> int:
        result = await self.session.execute(
            select(func.sum(Bet.amount))
        )
        return result.scalar_one() or 0
    
    async def get_total_won(self) -> int:
        result = await self.session.execute(
            select(func.sum(Bet.amount)).where(Bet.status == "won")
        )
        return result.scalar_one() or 0
    
    async def get_total_lost(self) -> int:
        result = await self.session.execute(
            select(func.sum(Bet.amount)).where(Bet.status == "lost")
        )
        return result.scalar_one() or 0


class AdminLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def log_action(
        self,
        admin_id: int,
        action: str,
        description: str,
        target_user_id: Optional[int] = None
    ) -> AdminAction:
        log = AdminAction(
            admin_id=admin_id,
            action=action,
            description=description,
            target_user_id=target_user_id
        )
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log
    
    async def get_recent_logs(self, limit: int = 50) -> List[AdminAction]:
        result = await self.session.execute(
            select(AdminAction)
            .order_by(desc(AdminAction.created_at))
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_admin_logs(self, admin_id: int, limit: int = 50) -> List[AdminAction]:
        result = await self.session.execute(
            select(AdminAction)
            .where(AdminAction.admin_id == admin_id)
            .order_by(desc(AdminAction.created_at))
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def count_logs(self) -> int:
        result = await self.session.execute(
            select(func.count(AdminAction.id))
        )
        return result.scalar_one()


# Алиасы для совместимости
AdminRepository = UserRepository
