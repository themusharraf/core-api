import jwt
from models.user import UserRole
from core.config import settings
from schemas.user import TokenResponse
from core.exceptions import TokenError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from datetime import datetime, timedelta, UTC

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    :param plain_password:
    :param hashed_password:
    :return bool: True if the password is valid False otherwise:
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_tokens(user_id: int, role: UserRole) -> TokenResponse:
    """
    Generate both access and refresh JWT tokens for a user.
    :param user_id : Unique identifier of the user:
    :param role : Role assigned to the user (USER, ADMIN):
    :return {'access_token' 'refresh_token'}
    """
    now = datetime.now(UTC)

    access_exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_exp = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_payload = {
        "sub": str(user_id),
        "role": role.value,
        "type": "access",
        "exp": access_exp,
        "iat": now,
    }

    refresh_payload = {
        "sub": str(user_id),
        "role": role.value,
        "type": "refresh",
        "exp": refresh_exp,
        "iat": now,
    }

    access_token = jwt.encode(
        access_payload,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )

    refresh_token = jwt.encode(
        refresh_payload,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


def decode_jwt_token(token: str) -> tuple[int, UserRole, str]:
    """
    Decode a JWT token and extract user information and token type.
    :param token:
    :return:
    - user_id : ID of the user from the token:
    - role : User role from the token:
    - token_type : Type of the token ('access', 'refresh'):
    """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not verify user credentials",
                                          )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM])

        user_id = payload.get("sub")
        role = payload.get("role")
        token_type = payload.get("type")

        if user_id is None:
            raise TokenError("Token 'sub' field is missing")
        if token_type is None:
            raise TokenError("Token 'type' field is missing")

        return int(user_id), UserRole(role), token_type

    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.PyJWKError:
        raise credentials_exception
