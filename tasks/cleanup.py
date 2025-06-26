from celery import shared_task
from core.db import async_session_maker
from sqlalchemy import select
from models.user import User
from core.enum import UserStatus
from core.logger import logger
from datetime import datetime, timedelta, UTC
import asyncio


@shared_task(name="tasks.cleanup.delete_old_unverified_users")
def delete_old_unverified_users():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_delete_old_unverified_users())
    except Exception as e:
        logger.error(f"Cleanup task failed: {e}")


async def _delete_old_unverified_users():
    logger.info("Cleanup task started...")
    async with async_session_maker() as session:
        before_time = datetime.now(UTC) - timedelta(days=2)

        stmt = select(User).where(User.status == UserStatus.UNVERIFIED,User.created_at <= before_time)
        result = await session.execute(stmt)
        users_to_delete = result.scalars().all()

        count = len(users_to_delete)

        for user in users_to_delete:
            await session.delete(user)

        await session.commit()
        logger.info(f"Deleted {count} unverified users older than 2 days.")
