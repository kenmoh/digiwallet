import uuid
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


from app.models.models import Wallet, TopUpWallet, User
from app.schemas.topup import TopUpSchema
from app.database.database import session
from app.utils import error_response
from app.utils.utils import get_payment_link


def top_up_db_wallet(wallet_address: uuid.UUID, top_up: TopUpSchema, user: User, db: session):
    db_wallet = db.query(Wallet).filter(Wallet.wallet_address == wallet_address).first()
    if not db_wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{db_wallet.id} not Found')

    if top_up.amount <= 500:
        error_response.invalid_exception('Invalid amount. Please enter a minimum amount of N 500!')
    try:
        with session.begin():
            new_top_up = TopUpWallet(
                amount=top_up.amount,
                user_id=user.id,
                wallet_address=db_wallet.wallet_address,
                created_at=datetime.today()
            )

            db.add(new_top_up)
            db.commit()
            db.refresh(new_top_up)

            new_top_up.payment_url = get_payment_link(new_top_up, user)
            db.commit()
            db.refresh(new_top_up)

            db_wallet.balance += new_top_up.amount

            db.commit()
            db.refresh(db_wallet)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return db_wallet


def user_top_ups(user_id: str, db: Session):
    return db.query(TopUpWallet).filter(TopUpWallet.user_id == user_id).all()


def top_up_details(top_up_id: str, db: Session):
    return db.query(TopUpWallet).filter(TopUpWallet.id == top_up_id).first()

