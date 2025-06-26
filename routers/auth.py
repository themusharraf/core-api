from schemas.base import BaseResponse
from dependencies.database import DBSession
from fastapi import APIRouter, HTTPException, status
from services.user import create_user, get_user_by_email, verify_user_account
from schemas.user import UserCreate, UserLogin, RefreshRequest, VerifyRequest, UserStatus
from core.security import verify_password, create_jwt_tokens, decode_jwt_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"])


@router.post(
    "/signup",
    response_model=BaseResponse,
    summary="Register a new user",
    description="""This endpoint registers a new user with the provided user data
     such as first_name (optional), last_name (optional), email, and password."""
)
async def signup_user(user_data: UserCreate, db: DBSession):
    result = await create_user(db, user_data)
    return BaseResponse(data=result)


@router.post(
    "/login",
    response_model=BaseResponse,
    summary="Log in a user",
    description="""This endpoint authenticates the user with their email 
    and password and returns access and refresh JWT tokens upon success."""
)
async def login(user_data: UserLogin, db: DBSession):
    user = await get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or password is incorrect")
    elif user.status == UserStatus.UNVERIFIED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is not verified. Please verify your email to proceed."
        )
    tokens = create_jwt_tokens(user.id, user.role)
    return BaseResponse(data=tokens)


@router.post(
    "/refresh",
    response_model=BaseResponse,
    summary="Refresh access token",
    description="""This endpoint accepts a valid refresh token and returns a new access token.
    The refresh token must not be expired."""
)
async def refresh_token_router(request: RefreshRequest):
    user_id, role, token_type = decode_jwt_token(request.refresh_token)
    if token_type != "refresh":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This token is not a refresh token")
    new_tokens = create_jwt_tokens(user_id=user_id, role=role)
    return BaseResponse(data={"access_token": new_tokens.access_token})


@router.post(
    "/verify",
    response_model=BaseResponse,
    summary="Verify user account",
    description="This endpoint verifies a user's account using the verification code sent to them during registration."
)
async def verify_account(request: VerifyRequest, db: DBSession):
    await verify_user_account(db, request.code)
    return BaseResponse(data={"message": "Account successfully verified"})
