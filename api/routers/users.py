from datetime import timedelta
from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
import logging
from authenticator import (
    authenticator,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from models import DatabaseError, Token, UserIn, UserOut
from queries.users import UsersRepo

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/api/users",
    response_model=UserOut | List[UserOut]
)
async def get_user(
    username: str = None,
    repo: UsersRepo = Depends()
):
    user = repo.get_user(username)
    if isinstance(user, DatabaseError):
        logger.error(DatabaseError)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error: " + user.failure,
        )
    if isinstance(user, list):
        return user
    if not isinstance(user, UserOut):
        logger.info(f"Could not find user with username: {username}")
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
):
    user.password = authenticator.get_hashed_password(user.password)
    user_out = repo.create_user(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    logger.debug(user)
    access_token = create_access_token(
        data={"sub": user_out}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
