import random
from models.user import VerifyCode
from datetime import datetime, timedelta, UTC
from dependencies.database import DBSession


def generate_code() -> str:
    return str(random.randint(100000, 999999))


async def create_verify_code(db: DBSession, user_id: int) -> str:
    """
    :param db:
    :param user_id:
    :return code:
    """
    code = generate_code()
    expires_at = datetime.now(UTC) + timedelta(minutes=1)
    verify_code = VerifyCode(code=code, user_id=user_id, expires_at=expires_at)
    db.add(verify_code)

    await db.commit()

    return code
