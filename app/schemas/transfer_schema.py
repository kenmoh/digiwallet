import decimal
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class TransferSchema(BaseModel):
    amount: decimal.Decimal = Field(ge=500)


class TransferResponseSchema(TransferSchema):
    id: str
    user_id: str
    wallet_id: uuid.UUID
    wallet_address: uuid.UUID
    created_at: datetime
    username: str
