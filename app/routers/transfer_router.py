import uuid

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.schemas.transfer_schema import TransferSchema, TransferResponseSchema
from app.models.models import User
from app.schemas.wallet_schema import WalletResponseSchema
from app.database.database import get_db
from app.services import transfer
from app.utils.auth import get_current_user


transfer_router = APIRouter(prefix='/api/transfers', tags=['Transfer'])


@transfer_router.get('', status_code=status.HTTP_200_OK)
def get_all_users_transfers(db: Session = Depends(get_db)) -> list[TransferResponseSchema]:
    return transfer.all_transfers(db)


@transfer_router.get('/user-transfers', status_code=status.HTTP_200_OK)
def get_user_transfers(user_id: str, db: Session = Depends(get_db)) -> list[TransferResponseSchema]:
    return transfer.user_transfers(user_id, db)


@transfer_router.post('', status_code=status.HTTP_201_CREATED)
def transfer_to_user(wallet_address: uuid.UUID, trans: TransferSchema, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)) -> WalletResponseSchema:
    return transfer.make_transfer(wallet_address, trans, current_user, db)


@transfer_router.get('/{transfer_id}', status_code=status.HTTP_200_OK)
def get_transfer_details(transfer_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> TransferResponseSchema:
    return transfer.transfer_details(transfer_id, db)
