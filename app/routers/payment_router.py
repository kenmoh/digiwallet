import uuid

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.schemas.payment_schema import PaymentSchema, PaymentResponseSchema
from app.models.models import User
from app.schemas.wallet_schema import WalletResponseSchema
from app.database.database import get_db
from app.services import payment
from app.utils.auth import get_current_user


payment_router = APIRouter(prefix='/api/payments', tags=['Payments'])


@payment_router.post('', status_code=status.HTTP_201_CREATED)
def pay_from_wallet(wallet_address: uuid.UUID, pay: PaymentSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> WalletResponseSchema:

    return payment.pay_with_wallet(wallet_address=wallet_address, pay=pay, user=current_user, db=db)


@payment_router.get('/{payment_id}', status_code=status.HTTP_200_OK)
def get_payment_details(payment_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> PaymentResponseSchema:
    return payment.payment_details(payment_id, db, current_user)
