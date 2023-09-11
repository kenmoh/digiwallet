from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import database
from app.models import models
from app.schemas import user_schema
from app.utils import error_response, utils, auth


login_router = APIRouter(prefix="/api", tags=["Login"])


@login_router.post("/login", response_model=user_schema.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username.lower())
        .first()
    )

    if not user:
        error_response.invalid_exception("Invalid Credentials!")

    if not utils.verify_password(user_credentials.password, user.password):
        error_response.invalid_exception("Invalid Credentials!")

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    access_token = auth.create_access_token(data=user_data)

    return {"access_token": access_token, "token_type": "bearer"}

