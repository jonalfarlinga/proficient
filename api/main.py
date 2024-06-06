from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from routers.users import router as user_router
from routers.auth import router as auth_router

if os.environ.get('LOGGING') == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)
elif os.environ.get('LOGGING') == "DETAIL":
    logging.basicConfig(filename="api_log", level=logging.INFO)
else:
    logging.basicConfig(filename="api_log", level=logging.WARNING)

logger = logging.getLogger(__name__)
app = FastAPI()
logger.debug("fastapi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ["CORS_HOST"]].
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.debug("cors")


app.include_router(user_router, tags=["Users"])
app.include_router(auth_router, tags=["Auth"])
logger.debug("done")
