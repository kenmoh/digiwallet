import uuid

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session


from app.schemas.topup import TopUpSchema, TopUpResponseSchema
from app.models.models import User
from app.schemas.wallet_schema import WalletResponseSchema
from app.database.database import get_db
from app.services import topup_wallet
from app.utils.auth import get_current_user
from app.utils import error_response

top_up_router = APIRouter(prefix='/api/top-up', tags=['Top Up'])


@top_up_router.get('', status_code=status.HTTP_200_OK)
def get_user_top_ups(user_id: str, db: Session = Depends(get_db)) -> list[TopUpResponseSchema]:
    return topup_wallet.user_top_ups(user_id, db)


@top_up_router.post('/{wallet_address}', status_code=status.HTTP_201_CREATED)
def top_up_wallet(wallet_address: uuid.UUID, top_up: TopUpSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> WalletResponseSchema:
    if current_user.wallet.wallet_address == wallet_address:
        return topup_wallet.top_up_db_wallet(wallet_address=wallet_address, top_up=top_up, db=db, user=current_user)


@top_up_router.get('/{top_up_id}', status_code=status.HTTP_200_OK)
def get_top_up_details(top_up_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> TopUpResponseSchema:
    if not current_user:
        error_response.invalid_exception('Unauthorized')
    return topup_wallet.top_up_details(top_up_id, db)
