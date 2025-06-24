from enum import StrEnum


class UserRole(StrEnum):
    """
    User role.
    """
    USER = "user"
    ADMIN = "admin"

    @classmethod
    def has_value(cls, value):
        return any(value == item for item in cls)


class UserStatus(StrEnum):
    """
    User status.
    """
    UNVERIFIED = "unverified"
    VERIFIED = "verified"

    @classmethod
    def has_value(cls, value):
        return any(value == item for item in cls)
