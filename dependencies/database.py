from fastapi import Depends
from typing import Annotated
from core.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession

DBSession = Annotated[AsyncSession, Depends(get_session)]
