from schemas.base import BaseResponse
from schemas.user import UserDetail, UserRole, UserUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from services.admin import admin_required
from dependencies.auth import get_current_user
from dependencies.database import DBSession
from pydantic import TypeAdapter
from sqlalchemy import select
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["User"])


@router.get(
    "/me",
    response_model=BaseResponse,
    summary="Get current user profile",
    description="Returns the profile details of the currently authenticated user."
)
async def get_user(current_user: User = Depends(get_current_user)):
    user_response = UserDetail.model_validate(current_user)
    return BaseResponse(data=user_response)


@router.get(
    "/",
    response_model=BaseResponse,
    summary="Get all users",
    description="Returns a list of all users in the system. Admin access is required."
)
async def get_users(db: DBSession, current_user: User = Depends(admin_required)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    user_data = TypeAdapter(list[UserDetail]).validate_python(users)
    return BaseResponse(data=user_data)


@router.get(
    "/{id}",
    response_model=BaseResponse,
    summary="Get user by ID",
    description="Fetch a user's details by their unique ID. Admin access is required."
)
async def user_about(id: int, db: DBSession, current_user: User = Depends(admin_required)):
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id={id} user not found.")
    return BaseResponse(data=UserDetail.model_validate(user))


@router.patch(
    "/{id}",
    response_model=BaseResponse,
    summary="Update user profile",
    description="Allows a user to update their own profile. Admins can update any user's profile."
)
async def get_update(id: int, user_update: UserUpdate, db: DBSession, current_user: User = Depends(get_current_user)):
    if current_user.id != id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this user's information.",
        )

    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id={id} user not found.")

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return BaseResponse(data=UserDetail.model_validate(user))


@router.delete(
    "/{id}",
    response_model=BaseResponse,
    summary="Delete user by ID",
    description="Deletes a user account by ID. Admin access is required."
)
async def user_delete(id: int, db: DBSession, current_user: User = Depends(admin_required)):
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id={id} user not found.")
    await db.delete(user)
    await db.commit()
    return BaseResponse(data=status.HTTP_204_NO_CONTENT)
