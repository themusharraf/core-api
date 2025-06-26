from models.user import User
from schemas.user import UserRole
from dependencies.auth import get_current_user
from fastapi import Depends, HTTPException, status


async def admin_required(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that ensures the current user is an admin.
    :param current_user:
    :return User: The same user instance if the role is ADMIN:
    :raises HTTPException: If the user's role is not ADMIN (403 Forbidden):
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin users are allowed.")
    return current_user
