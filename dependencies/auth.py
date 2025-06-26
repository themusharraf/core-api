from typing import Annotated
from models.user import User
from sqlalchemy import select
from core.security import decode_jwt_token
from dependencies.database import DBSession
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

http_bearer = HTTPBearer()


async def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)], db: DBSession) -> User:
    """
    :param token:
    :param db:
    :return User: The authenticated user instance from the database:
    :raises HTTPException: If the token is invalid or the user is not found:
    """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="User authentication failed.")
    try:
        user_id, _, _ = decode_jwt_token(token.credentials)
    except Exception:
        raise credentials_exception
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
