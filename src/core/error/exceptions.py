from fastapi import status


class CustomException(Exception):
    code = status.HTTP_502_BAD_GATEWAY
    message = "Bad Gateway"

    def __init__(self, errors: dict[str, str] | str | None = None, message: str | None = None):
        self.errors = errors
        self.message = message or self.message

    def __str__(self) -> str:
        return f"{self.message} -> {self.errors}"


class DatabaseError(CustomException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Database Error"


class ValidationException(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    message = "Validation failed"


class NotFoundException(CustomException):
    code = status.HTTP_404_NOT_FOUND
    message = "Not found"


class JWTError(CustomException):
    code = status.HTTP_403_FORBIDDEN
    message = "Not authenticated"


class RequestError(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    message = "Request error"


class MaintenanceModeException(CustomException):
    code = status.HTTP_403_FORBIDDEN
    message = "Maintenance Mode"


class UpdateRequiredException(CustomException):
    code = status.HTTP_403_FORBIDDEN
    message = "Update Required"
