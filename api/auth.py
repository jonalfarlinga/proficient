from fastapi import Depends
from models import UserOut, UserOutWithPassword, DatabaseError
from queries.users import UsersRepo
from passlib.hash import pbkdf2_sha256


class Authenticator:
    def __init__(self, key: str):
        self.key = key

    def get_account_data(
            self,
            email: str,
            users: UsersRepo
    ) -> UserOut:
        return users.get(email)

    def get_account_getter(
            self,
            users: UsersRepo = Depends(),
    ) -> UsersRepo:
        return users

    def get_hashed_password(self, password: str) -> str:
        hashed_password = pbkdf2_sha256.hash(password)
        return hashed_password

    def verify_password(
            self,
            email: str,
            password: str,
            users: UsersRepo = Depends()
    ) -> bool | DatabaseError:
        user_password = users.get_password(email)
        if not isinstance(user_password, UserOutWithPassword):
            return user_password
        return pbkdf2_sha256.verify(password, user_password)
