from datetime import datetime
import uuid
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DECIMAL, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.utils.utils import unique_id, api_key_gen, api_test_key_gen
from app.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True, default=unique_id)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    wallet: Mapped['Wallet'] = relationship('Wallet', uselist=False, back_populates="user", cascade="all, delete-orphan")
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    api_key: Mapped[str] = mapped_column(String, default=api_key_gen, unique=True, nullable=True)
    api_test_key: Mapped[str] = mapped_column(String, default=api_test_key_gen, unique=True, nullable=True)

    def __str__(self):
        return f'{self.username}'


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=unique_id)
    wallet_address: Mapped[uuid] = mapped_column(UUID, default=uuid.uuid1)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    username: Mapped[str]
    user: Mapped[User] = relationship("User", back_populates="wallet")
    payments: Mapped[str] = relationship("Payment", back_populates="wallet")
    transfers: Mapped['Transfer'] = relationship("Transfer", back_populates="wallet")
    balance: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'{self.wallet_address} -> {self.user}'


class TopUpWallet(Base):
    __tablename__ = 'topups'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=unique_id)
    wallet_address: Mapped[uuid.UUID]
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False, default=0.0)
    payment_url: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'{self.wallet_address} -> {self.amount}'


class Transfer(Base):
    __tablename__ = 'transfers'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=unique_id)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    wallet_id: Mapped[str] = mapped_column(String, ForeignKey("wallets.id"), nullable=False)
    wallet_address: Mapped[uuid.UUID]
    username: Mapped[str]
    wallet: Mapped[str] = relationship("Wallet", back_populates="transfers")
    amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'{self.wallet_address} -> {self.amount}'


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=unique_id)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    wallet_id: Mapped[str] = mapped_column(String, ForeignKey("wallets.id"), nullable=False)
    wallet_address: Mapped[uuid.UUID]
    wallet: Mapped[str] = relationship("Wallet", back_populates="payments")
    amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False, default=0.0)
    merchant: Mapped[str] = mapped_column(default='Kenneth', nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'{self.wallet_address} -> {self.amount}'


class Withdraw(Base):
    __tablename__ = 'withdrawals'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=unique_id)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('user.id'), nullable=False)