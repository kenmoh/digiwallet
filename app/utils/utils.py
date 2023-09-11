import secrets
import uuid

from passlib.context import CryptContext
import requests

from app.config.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return password_context.hash(password)


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def unique_id():
    return str(uuid.uuid1()).replace("-", "")


def api_key_gen():
    return secrets.token_hex(32)


def api_test_key_gen():
    return secrets.token_hex(12)


# GET PAYMENT LINK
def get_payment_link(top_up, current_user):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {"Authorization": f"Bearer {settings.FLW_SECRET_KEY}"}
    details = {
        "tx_ref": top_up.id,
        "amount": str(top_up.amount),
        "currency": "NGN",
        "redirect_url": "https://mohdelivery.onrender.com/api/payment/callback",
        "customer": {
            "email": current_user.email,
            "username": current_user.username,
        },
    }

    response = requests.post(url, json=details, headers=headers)
    response_data = response.json()
    link = response_data["data"]["link"]

    return link
