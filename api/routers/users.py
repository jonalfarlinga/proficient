from datetime import timedelta
from typing import Annotated, List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
import logging

from fastapi.security import OAuth2PasswordRequestForm
from authenticator import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_authenticator
)
from models import DatabaseError, Token, UserIn, UserOut, UserUpdate
from queries.users import UsersRepo

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/api/users",
    response_model=UserOut | List[UserOut]
)
async def get_user(
    email: str = None,
    repo: UsersRepo = Depends()
):
    """
    Retrieve a list of users in the database.

    - Optionally, submit a query parameter:
      - "email": a user's email
      - **E.G.** `/api/users?email=test@example.com`
    - If called without a query string, returns a JSON-format list of all users
    - If an email query is supplied, returns a JSON object respresenting the
    associated user
    - If an email query is supplied, but no associated account is found,
    returns a 404 error
    """
    user = repo.get_user(email)
    if isinstance(user, DatabaseError):
        logger.error(DatabaseError)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error: " + user.failure,
        )
    if isinstance(user, list):
        return user
    if not isinstance(user, UserOut):
        logger.info(f"Could not find user with username: {email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )
    return user


@router.post(
    "/api/users", response_model=Token)
def create_user_end(
    user: UserIn,
    repo: UsersRepo = Depends(),
    authenticator=Depends(get_authenticator),
):
    """
    Creates a new user in the datase.

    - Submit a JSON body including:
      - "email": string, must be unique and not null,
      - "username": string, must be unique and not null,
      - "name": string, must not be null,
      - "password": string, must not be null
    - If successful, authorizes the created user and returns a JSON object
    containing "access_token", "token_type", and "user" attributes
    """
    user.password = authenticator.get_hashed_password(user.password)
    user_out = repo.create_user(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    logger.debug(user)
    access_token = create_access_token(
        data={"sub": user_out}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer", user=user_out)


@router.put(
    "/api/users", response_model=UserOut)
def update_user_end(
    user: UserUpdate,
    repo: UsersRepo = Depends(),
    authenticator=Depends(get_authenticator)
):
    """
    Updates a user in the database with new data.

    - Submit a JSON body including:
      - "email": string, must be unique and not null,
      - "username": string, must be unique and not null,
      - "name": string, must not be null,
      - "password": string, must not be null,
      - "new_password": string, leave null if password is not to be changed,
      - "new_email": string, leave null if email is not to be changed
    - The "email" and "password" are checked against users in the database. If
    a match is found, then the database is updated with the full user data,
    using "new_email" and "new_password" if they are supplied.
    """
    stored_user = authenticator.verify_password(
        user.email,
        user.password,
        repo
    )
    if not stored_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.new_email:
        user.email = user.new_email
    if user.new_password:
        user.password = authenticator.get_hashed_password(user.new_password)
    else:
        user.password = authenticator.get_hashed_password(user.password)
    user_out = repo.update_user(stored_user.id, user)
    if isinstance(user_out, DatabaseError):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Failed to update user:\n" + user_out.detail
        )
    return user_out
