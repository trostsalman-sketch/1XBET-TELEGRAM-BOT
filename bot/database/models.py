from sqlalchemy import BigInteger, String, Integer, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Telegram ID как primary key
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    
    # Relationships
    bets: Mapped[List["Bet"]] = relationship("Bet", back_populates="user")
    admin_actions: Mapped[List["AdminAction"]] = relationship("AdminAction", back_populates="admin", foreign_keys="AdminAction.admin_id")

class Bet(Base):
    __tablename__ = "bets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    game: Mapped[str] = mapped_column(String(20), nullable=False)  # basketball, football, fortune
    choice: Mapped[str] = mapped_column(String(50), nullable=False)  # variant1, variant2, red, black, green
    result: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")  # pending, active, won, lost, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False), nullable=True)
    transaction_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('amount >= 10000', name='check_min_amount'),
    )
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="bets")

class AdminAction(Base):
    __tablename__ = "admin_actions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    admin_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    target_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    
    # Relationships
    admin: Mapped["User"] = relationship("User", foreign_keys=[admin_id])
