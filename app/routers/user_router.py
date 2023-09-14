from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserResponseSchema, CreateUserSchema
from app.database.database import get_db
from app.services import user


user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.get('', status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)) -> list[UserResponseSchema]:

    """
    - List all users
    """
    return user.get_users(db)


@user_router.post('', status_code=status.HTTP_201_CREATED)
def register_user(db_user: CreateUserSchema, db: Session = Depends(get_db)) -> UserResponseSchema:

    """
    - Add new user
    """
    return user.create_user(db_user, db)


@user_router.get('/{user_id}', status_code=status.HTTP_200_OK)
def get_single_user(user_id: str, db: Session = Depends(get_db)) -> UserResponseSchema:

    """
    - Get user
    """
    return user.get_user(user_id, db)


@user_router.patch('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: str, db_user: CreateUserSchema, db: Session = Depends(get_db)) -> UserResponseSchema:

    """
    - Update a user
    """
    return user.update_db_user(user_id, db_user, db)


@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)) -> None:

    """
    - Delete a user
    """
    return user.delete_db_user(user_id, db)
