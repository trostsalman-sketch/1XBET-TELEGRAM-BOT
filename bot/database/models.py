from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, Integer, Boolean, Text, TIMESTAMP, ForeignKey, CheckConstraint, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(255))
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    block_reason: Mapped[Optional[str]] = mapped_column(Text)
    blocked_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
    blocked_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    bets: Mapped[list["Bet"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Admin(Base):
    __tablename__ = "admins"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    appointed_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    appointed_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

class Bet(Base):
    __tablename__ = "bets"
    __table_args__ = (
        CheckConstraint('amount >= 10000', name='check_min_amount'),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    game: Mapped[str] = mapped_column(String(20), nullable=False)
    choice: Mapped[str] = mapped_column(String(50), nullable=False)
    result: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='pending')
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
    transaction_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    
    user: Mapped["User"] = relationship(back_populates="bets")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    bet_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("bets.id"))
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='pending')
    external_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

class AdminLog(Base):
    __tablename__ = "admin_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    target_user_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    details: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
