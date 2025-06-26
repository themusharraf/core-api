from enum import StrEnum


class UserRole(StrEnum):
    """
    User role.
    """
    USER = "user"
    ADMIN = "admin"


class UserStatus(StrEnum):
    """
    User status.
    """
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
