from datetime import datetime
import decimal
import uuid

from pydantic import BaseModel


class WalletResponseSchema(BaseModel):
    id: str
    wallet_address: uuid.UUID
    user_id: str
    balance: decimal.Decimal
    created_at: datetime
