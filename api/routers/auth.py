from datetime import timedelta
from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordRequestForm
from models import Token, UserOut
from queries.users import UsersRepo
import logging
from authenticator import (
    authenticator,
    get_current_active_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    repo: UsersRepo = Depends()
) -> Token:

    user = authenticator.verify_password(
        form_data.username,
        form_data.password,
        repo

    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    logger.debug(user)
    access_token = create_access_token(
        data={"sub": user}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/token", response_model=UserOut)
async def get_token(
    current_user: Annotated[
        UserOut,
        Depends(get_current_active_user)
    ],
):
    return current_user
