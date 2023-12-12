from datetime import datetime
from authlib.jose import jwt
from fastapi import Header
from werkzeug.security import generate_password_hash, check_password_hash

from controllers.requests import unauthorized_response

SECRET_KEY = "javainuse-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


def verifyToken(token, secret_key):
    token = token.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        if payload.get("exp") < datetime.datetime.utcnow().timestamp():
            return unauthorized_response("Token is expired")
        return payload
    except jwt.ExpiredSignatureError:
        return unauthorized_response("Token is expired")
    except jwt.InvalidTokenError:
        return unauthorized_response("Token is invalid")
    except Exception as e:
        return unauthorized_response(str(e))


def verifyUserToken(token: str = Header(None)):
    if not token:
        return unauthorized_response("Token is required")

    verifyToken(token, SECRET_KEY)
    return None


def generateToken(payload, secret_key, expiration_minutes=30):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    token = jwt.encode({
        "exp": expiration_time,
        **payload},
        secret_key,
        algorithm="HS256"
    )
    return token


def PasswordHash(password):
    return generate_password_hash(password)


def PasswordCheck(provided_password, hashed_password):
    return check_password_hash(hashed_password, provided_password)
