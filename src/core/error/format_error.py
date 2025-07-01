from src.core.error.codes import (
    FORBIDDEN_ERROR,
    INTERNAL_ERROR,
    INVALID_CRED,
    INVALID_USER,
    LOCK_ERROR,
    MAINTENANCE_MODE,
    NO_DATA,
    NOT_AUTHORIZED,
    SERVICE_UNAVAILABLE,
    TOO_MANY_REQUESTS,
    UNAUTHORIZED_ERROR,
    UPDATE_REQUIRED,
    USER_EXISTS,
)

ERROR_MAPPER = {
    USER_EXISTS: "User with this phone number already exists",
    INVALID_USER: "Your account is invalid. Please contact Support",
    NO_DATA: "No data found",
    SERVICE_UNAVAILABLE: "This service is currently unavailable",
    UNAUTHORIZED_ERROR: "Unauthorized",
    FORBIDDEN_ERROR: "Forbidden",
    INTERNAL_ERROR: "Internal Server Error",
    INVALID_CRED: "Invalid credentials",
    NOT_AUTHORIZED: "You are not authorized to perform this action",
    MAINTENANCE_MODE: "Maintenance mode",
    UPDATE_REQUIRED: "Update required",
    TOO_MANY_REQUESTS: "Too many requests",
    LOCK_ERROR: "Lock error",
}


def field_error_format(errors: list[dict[str, str]]) -> dict[str, str]:
    formatted_errors: dict[str, str] = {}

    for error in errors:
        try:
            field_name = error.get("loc", ["N/A", "N/A"])[1]
        except IndexError:
            field_name = "N/A"

        error_type = error.get("type", "")
        if error_type == "missing":
            formatted_errors[field_name] = f"{field_name} is required"
        elif error_type == "value_error":
            parts = error.get("msg", "").split(",")
            code = parts[1].strip() if len(parts) > 1 else "unknown"
            message = ERROR_MAPPER.get(code, "Unknown error")
            formatted_errors[field_name] = message
        else:
            formatted_errors[field_name] = error.get("msg", "Unknown error")

    return formatted_errors
