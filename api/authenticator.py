from datetime import timedelta, datetime, timezone
import json
import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models import UserOut, DatabaseError
from queries.users import UsersRepo
from passlib.hash import pbkdf2_sha256
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SIGNING_KEY = os.environ["SIGNING_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Authenticator:
    def __init__(self, key: str):
        self.key = key

    def get_account_data(
            self,
            username: str,
            users: UsersRepo
    ) -> UserOut:
        return users.get(username)

    def get_hashed_password(self, password: str) -> str:
        hashed_password = pbkdf2_sha256.hash(password)
        return hashed_password

    def verify_password(
            self,
            username: str,
            password: str,
            users: UsersRepo
    ) -> bool | DatabaseError:
        user_password = users.get_password(username)
        verified = pbkdf2_sha256.verify(password, user_password)
        if verified:
            return users.get_user(username)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    to_encode = {'sub': json.dumps(data["sub"].dict())}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SIGNING_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repo: UsersRepo = Depends()
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SIGNING_KEY, algorithms=[ALGORITHM])
        user: str = json.loads(payload.get("sub"))
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserOut, Depends(get_current_user)],
):
    print(current_user)
    return current_user


authenticator = Authenticator(SIGNING_KEY)
