from fastapi import HTTPException, status


class TokenError(Exception):
    pass


verification_failed_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid verification code"
)

verification_expired_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Verification code has expired"
)
