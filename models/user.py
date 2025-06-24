from sqlalchemy import BigInteger, VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, validates
from email_validator import validate_email, EmailNotValidError
from models.base import BaseModel


class User(BaseModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(VARCHAR(255))

    @validates('email')
    def validate_email_address(self, address):
        """
            Validate email format using the email-validator library.
            Raises:
                ValueError: If the email is invalid.
            Returns:
                str: Validated email address.
        """
        try:
            validate_email(address)
        except EmailNotValidError as e:
            raise ValueError(str(e))
        return address
