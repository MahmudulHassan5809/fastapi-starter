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

ERROR_MAPPER = {
    INVALID_PHONE: {
        "en": "Invalid phone number",
        "bn": "অচল ফোন নম্বর",
    },
    OTP_NOT_SENT: {"en": "Can not set otp", "bn": "ওটিপি সেট করা যাবে না"},
    USER_EXISTS: {
        "en": "User with this phone number already exists",
        "bn": "এই ফোন নম্বর সহ ব্যবহারকারী ইতিমধ্যেই বিদ্যমান৷",
    },
    INVALID_USER: {
        "en": "Your account is invalid. Please contact Support",
        "bn": "আপনার অ্যাকাউন্টটি অকার্যকর করা হয়েছে । অনুগ্রহ করে হেল্পলাইনে যোগাযোগ করুন",
    },
    INVALID_OTP: {"en": "Invalid otp", "bn": "অকার্যকর ওটিপি"},
    INVALID_CRED: {
        "en": "Incorrect phone number or pin",
        "bn": "ভুল ফোন নম্বর বা পিন",
    },
    FORBIDDEN_ERROR: {"en": "Forbidden", "bn": "Forbidden", "field": "auth"},
    NO_DATA: {
        "en": "No data found",
        "bn": "কোন তথ্য পাওয়া যায়নি",
    },
    INVALID_DATA: {
        "en": "Invalid data",
        "bn": "অবৈধ তথ্য",
        "field": "",
    },
    INTERNAL_ERROR: {
        "en": "Please try again later",
        "bn": "অনুগ্রহ করে পরে আবার চেষ্টা করুন",
    },
    TOO_MANY_REQUEST: {
        "en": "Please try after some time",
        "bn": "অনুগ্রহ করে কিছু সময় পরে আবার চেষ্টা করুন",
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
