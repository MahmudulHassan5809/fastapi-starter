import bcrypt


class PasswordHandler:
    @staticmethod
    def hash(password: str) -> str:
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        string_password = hashed_password.decode("utf8")
        return str(string_password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        password_byte_enc = plain_password.encode("utf-8")
        hashed_password_bytes = hashed_password.encode("utf-8")
        return bool(bcrypt.checkpw(password_byte_enc, hashed_password_bytes))