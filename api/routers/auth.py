from datetime import timedelta
from typing import Annotated, Dict
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status
)
from fastapi.security import OAuth2PasswordRequestForm
from models import Token, UserOut
from queries.users import UsersRepo
import logging
from authenticator import (
    get_authenticator,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    response: Response,
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    repo: UsersRepo = Depends(),
    authenticator=Depends(get_authenticator),
) -> Token:
    """
    "username" is email address
    """
    user = authenticator.verify_password(
        form_data.username,
        form_data.password,
        repo
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    logger.debug(user)
    access_token = create_access_token(
        data={"sub": user}, expires_delta=access_token_expires
    )
    response.set_cookie("authorization", "Bearer " + access_token)
    return Token(access_token=access_token, token_type="bearer", user=user)


@router.get("/token", response_model=Token)
async def get_token(
    current_user: Annotated[
        UserOut,
        Depends(get_current_user)
    ],
):
    return current_user
