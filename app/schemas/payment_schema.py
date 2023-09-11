from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, UUID1


class PaymentSchema(BaseModel):
    amount: Decimal


class PaymentResponseSchema(PaymentSchema):
    id: str
    user_id: str
    wallet_id: UUID1
    wallet_address: UUID1
    merchant: str | None
    created_at: datetime


