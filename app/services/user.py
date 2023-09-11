from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.models import User, Wallet
from app.database.database import session
from app.utils.error_response import user_data_already_exist
from app.utils import utils
from app.schemas.user_schema import CreateUserSchema


def get_users(db: session):
    try:
        return db.query(User).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def create_user(user: CreateUserSchema, db: Session):
    user_exist = user_data_already_exist(user, db)

    if user_exist:
        return user_exist

    try:
        with session.begin():
            new_user = User(
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                phone_number=user.phone_number,
                password=utils.hash_password(user.password),
                created_at=datetime.today()
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            wallet = Wallet(user_id=new_user.id, username=new_user.username, balance=0.00)

            db.add(wallet)
            db.commit()
            db.refresh(wallet)

            return new_user

    except IntegrityError as e:
        error_info = e.orig.args[0].split("\n")[0]
        if "users_phone_number_key" in error_info:
            raise HTTPException(status_code=409, detail="Phone number already exists")


def get_user(user_id: str, db: session):
    return db.query(User).filter(User.id == user_id).first()


def update_db_user(user_id: str, user: CreateUserSchema, db: session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{db_user.id} not Found')
    try:

        db_user.username = user.username
        db_user.email = user.email
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.phone_number = user.phone_number

        db.commit()
        db.refresh(db_user)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return db_user


def delete_db_user(user_id: str, db: session):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{db_user.id} not Found')

    db.delete(db_user)
    db.commit()
