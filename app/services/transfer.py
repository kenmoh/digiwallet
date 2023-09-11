import uuid
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


from app.models.models import Wallet, Transfer, User
from app.schemas.transfer_schema import TransferSchema
from app.database.database import session
from app.utils import error_response


def make_transfer(wallet_address: uuid.UUID, transfer: TransferSchema, user: User, db: session):
    transfer_to_wallet = db.query(Wallet).filter(Wallet.wallet_address == wallet_address).first()
    transfer_from_wallet = db.query(Wallet).filter(Wallet.wallet_address == user.wallet.wallet_address).first()
    if not transfer_to_wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{transfer_to_wallet.id} not Found')

    if transfer_from_wallet.balance == 0 or transfer_from_wallet.balance < transfer.amount:
        error_response.invalid_exception('Insufficient fund. Top up wallet!')

    if transfer_from_wallet.wallet_address == transfer_to_wallet.wallet_address:
        error_response.invalid_exception('Not allowed. You cannot transfer to your own wallet!')

    if transfer.amount <= 500:
        error_response.invalid_exception('Invalid amount. Please enter a minimum amount of N 500!')

    try:
        with session.begin():
            new_transfer = Transfer(
                amount=transfer.amount,
                user_id=user.id,
                username=user.username,
                wallet_id=user.wallet.id,
                wallet_address=transfer_to_wallet.wallet_address,
                created_at=datetime.today()
            )

            db.add(new_transfer)
            db.commit()
            db.refresh(new_transfer)

            transfer_to_wallet.balance += new_transfer.amount
            transfer_from_wallet.balance -= new_transfer.amount

            db.commit()
            db.refresh(transfer_to_wallet)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return transfer_from_wallet


def user_transfers(user_id: str, db: Session):
    return db.query(Transfer).filter(Transfer.user_id == user_id).all()


def transfer_details(transfer_id: str, db: Session):
    return db.query(Transfer).filter(Transfer.id == transfer_id).first()


def all_transfers(db: Session):
    return db.query(Transfer).all()
