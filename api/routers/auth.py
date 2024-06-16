from datetime import timedelta
from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
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


@router.post("/token", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    repo: UsersRepo = Depends(),
    authenticator=Depends(get_authenticator),
):
    """
    Log in to **PROF**icient teaching tools manager.

    - Submit a multipart form containing:
      - "username": an email address*,
      - "password": the associated user password
    - If successful, the response will be a JSON object containing
    "access_token", "token_type", and "user" attributes
    - If the username doesn't match a user, or the password doesn't match the
    that was found, returns a 401 error

    **NOTE**: username is an OAuth standard form field. Although it is titled
    username, PROFicient's login is based on the user's email. Users also have
    a "username" which is not related to the login method.
    """
    print(form_data.username)
    print(form_data.password)
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
    return Token(access_token=access_token, token_type="bearer", user=user)


@router.get("/token", response_model=Token)
async def get_token(
    current_user: Annotated[
        UserOut,
        Depends(get_current_user)
    ],
):
    """
    Gets the token for the current user.

    - Submit credentials as a header:
      - "authorization: "Bearer -token-"
    - If the token is valid, returns a JSON object containing
    "access_token", "token_type", and "user" attributes
    - If the authorization is missing or invalid, returns a 401 error
    """
    print(current_user)
    return current_user
