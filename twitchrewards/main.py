"""Wires available routes."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from twitchrewards.controllers import authentication_router, user_router

app = FastAPI()

# streamlabs make the request from multiple ports, making it hard
# to set a specific origin
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication_router)
app.include_router(user_router, prefix="/users")
