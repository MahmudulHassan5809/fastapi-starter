from src.core.error.codes import (
    FORBIDDEN_ERROR,
    INTERNAL_ERROR,
    INVALID_CRED,
    INVALID_DATA,
    INVALID_OTP,
    INVALID_PHONE,
    INVALID_USER,
    NO_DATA,
    OTP_NOT_SENT,
    TOO_MANY_REQUEST,
    USER_EXISTS,
)

# if you want add error msg in any language, please add it here
ERROR_MAPPER = {
    INVALID_PHONE: {
        "en": "Invalid phone number",
    },
    OTP_NOT_SENT: {
        "en": "Can not set otp",
    },
    USER_EXISTS: {
        "en": "User with this phone number or email already exists",
    },
    INVALID_USER: {
        "en": "Your account is invalid. Please contact Support",
    },
    INVALID_OTP: {
        "en": "Invalid otp",
    },
    INVALID_CRED: {
        "en": "Incorrect phone number or pin",
    },
    FORBIDDEN_ERROR: {
        "en": "Forbidden",
        "field": "auth",
    },
    NO_DATA: {
        "en": "No data found",
    },
    INVALID_DATA: {
        "en": "Invalid data",
        "field": "",
    },
    INTERNAL_ERROR: {
        "en": "Please try again later",
    },
    TOO_MANY_REQUEST: {
        "en": "Please try after some time",
        "field": "",
    },
}


def field_error_format(error: dict[str, str]) -> dict[str, str]:
    try:
        field_name = error["loc"][1]
    except IndexError:
        field_name = "N/A"
    error_type = error["type"]
    if error_type == "missing":
        return {
            "en": f"{field_name} is required",
            "bn": f"{field_name} is required",
            "field": field_name,
        }
    if error_type == "value_error":
        code = error["msg"].split(",")[1].strip()
        message = ERROR_MAPPER.get(code, {})
        message["field"] = message.get("field", field_name)
        return message
    return {
        "en": error.get("msg", "N/A"),
        "bn": error.get("msg", "N/A"),
        "field": field_name,
    }
