from fastapi import status, HTTPException


from app.models.models import User


def unauthorized_exception(message: str):
    """
     - Helper function that throws HTTPException when a user provide invalid credentials
    """
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{message}")


def invalid_exception(message: str):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{message}")


def not_found_exception(message: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{message} ",
    )


def user_data_already_exist(user, db):
    """
    - A helper function that checks if a use email, username, phone number already exist
    """
    email = db.query(User).filter(User.email == user.email).first()
    username = db.query(User).filter(User.username == user.username).first()
    phone_number = db.query(User).filter(User.phone_number == user.phone_number).first()

    if email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with that email already exists",
        )

    if username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with that username name already exists",
        )

    if phone_number is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with that phone number already exists",
        )
