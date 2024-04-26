from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from models import UserIn, UserOut
from queries.users import UsersRepo

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

logging.debug("fastapi")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ["CORS_HOST"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.debug("cors")


@app.get("/api/hello")
def hello_world():
    return {"hello": "world"}


@app.post("/api/users")
def create_user_end(
    user: UserIn,
    repo: UsersRepo = Depends()
):
    user_out = repo.create_user(user)
    return user_out


logging.debug("done")
