import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class TopUpSchema(BaseModel):
    amount: Decimal = Field(ge=500)


class TopUpResponseSchema(TopUpSchema):
    id: str
    user_id: str
    payment_url: str
    created_at: datetime
