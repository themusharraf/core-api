from datetime import datetime
from models.base import BaseModel
from core.enum import UserRole, UserStatus
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import mapped_column, Mapped, validates, relationship
from sqlalchemy import BigInteger, VARCHAR, DateTime, ForeignKey, Enum as SqlEnum


class User(BaseModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(VARCHAR(255))

    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.USER, nullable=False)
    status: Mapped[UserStatus] = mapped_column(SqlEnum(UserStatus), default=UserStatus.UNVERIFIED, nullable=False)

    verify_codes: Mapped[list["VerifyCode"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @validates('email')
    def validate_email_address(self, key, address):
        """
        :param key:
        :param address:
        :return str: The validated and normalized email address.:
        :raise ValueError: If the email address is not valid.:
        """
        try:
            validate_email(address)
        except EmailNotValidError as e:
            raise ValueError(str(e))
        return address


class VerifyCode(BaseModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(VARCHAR(6), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["User"] = relationship(back_populates="verify_codes", passive_deletes=True)
