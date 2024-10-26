from enum import Enum


class CacheTag(Enum):
    USER_DATA = """USER_DATA_{user_id}"""
    USER_ACCESS_TOKEN = """USER_ACCESS_TOKEN_{user_id}"""
    USER_REFRESH_TOKEN = """USER_REFRESH_TOKEN_{user_id}"""
