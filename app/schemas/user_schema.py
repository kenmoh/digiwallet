import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field


class BaseUserSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str


class CreateUserSchema(BaseUserSchema):
    password: str


class UserResponseSchema(BaseUserSchema):
    id: str
    created_at: datetime


class WalletResponseSchema(BaseModel):
    id: str
    wallet_address: uuid.UUID
    user_id: str
    user: str
    balance: Decimal = Field(decimal_places=2, default=0.00)
    created_at: datetime


class TokenData(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str
