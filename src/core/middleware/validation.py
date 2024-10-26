from fastapi import Request
from fastapi.exceptions import RequestValidationError

from src.core.error.exceptions import ValidationException
from src.core.error.format_error import field_error_format


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> None:
    details = exc.errors()
    errors = field_error_format(details[0])
    raise ValidationException(errors=errors)
