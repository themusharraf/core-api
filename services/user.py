from sqlalchemy import select
from datetime import datetime, UTC
from core.security import pwd_context
from models.user import User, VerifyCode
from fastapi import HTTPException, status
from core.enum import UserRole, UserStatus
from dependencies.database import DBSession
from schemas.user import UserCreate, UserDetail
from services.code_generate import create_verify_code
from tasks.email_tasks import send_verification_email
from core.exceptions import verification_expired_exception, verification_failed_exception


async def create_user(db: DBSession, user_data: UserCreate) -> UserDetail:
    """
    :param db:
    :param user_data:
    :return UserDetail: The newly created user serialized for response:
    :raises HTTPException: If a user with the given email already exists:
    """
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    hashed_password = pwd_context.hash(user_data.password)

    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=hashed_password,
        role=UserRole.USER,
        status=UserStatus.UNVERIFIED,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    code = await create_verify_code(db, user_id=new_user.id)
    send_verification_email.delay(user_data.email, code)

    return UserDetail.model_validate(new_user)


async def get_user_by_email(db: DBSession, email: str) -> User | None:
    """
    :param db:
    :param email:
    :return User | None: The user object if found otherwise None:
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def verify_user_account(db: DBSession, code: str) -> None:
    """
    :param db:
    :param code:
    :return:
    """
    result = await db.execute(select(VerifyCode).where(VerifyCode.code == code))
    verify_code = result.scalar_one_or_none()
    if not verify_code:
        raise verification_failed_exception
    if verify_code.expires_at < datetime.now(UTC):
        raise verification_expired_exception
    result = await db.execute(
        select(User).where(User.id == verify_code.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = UserStatus.VERIFIED
    await db.commit()
