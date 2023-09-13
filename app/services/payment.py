import uuid
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


from app.models.models import Wallet, Payment, User
from app.schemas.payment_schema import PaymentSchema
from app.database.database import session
from app.utils import error_response


def pay_with_wallet(wallet_address: uuid.UUID, pay: PaymentSchema, user: User, db: session):
    """
    - A helper function that allow user to pay with wallet
    """
    pay_to_wallet = db.query(Wallet).filter(Wallet.wallet_address == wallet_address).first()
    pay_from_wallet = db.query(Wallet).filter(Wallet.wallet_address == user.wallet.wallet_address).first()

    if pay_from_wallet.balance == 0 or pay_from_wallet.balance < pay.amount:
        error_response.invalid_exception('Insufficient fund. Top up wallet!')

    try:
        new_payment = Payment(
            amount=pay.amount,
            user_id=user.id,
            wallet_id=user.wallet.id,
            wallet_address=pay_to_wallet.wallet_address,
            merchant=pay_to_wallet.username,
            created_at=datetime.today()
        )

        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)

        pay_to_wallet.balance += new_payment.amount
        pay_from_wallet.balance -= new_payment.amount

        db.commit()
        db.refresh(pay_to_wallet)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return pay_from_wallet


def user_payments(db: Session, user: User):
    """
    - This helper function get user payment history from the database
    """
    return db.query(Payment).filter(Payment.user_id == user.id).all()


def payment_details(payment_id: str, db: Session, user: User):
    """
    - This helper function get payment details from the database
    """
    return db.query(Payment).filter(Payment.id == payment_id).filter(Payment.user_id == user.id).first()
