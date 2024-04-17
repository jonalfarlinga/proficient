from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

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


logging.debug("done")
