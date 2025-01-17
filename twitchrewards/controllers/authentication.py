"""Contains routes related to authentication"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, Response

from twitchrewards.services.authentication import AUTH_COOKIE_KEY, generate_token
from twitchrewards.controllers.view_models import AuthenticationData
router = APIRouter()

@router.get("/token")
def handle_twitch_redirect():
    return FileResponse("twitchrewards/views/authenticate.html")

@router.post("/token", status_code=status.HTTP_200_OK)
def authenticate(authentication_data: AuthenticationData, response: Response):
    """Gets JWT to perform write operations in the API"""
    access_token = generate_token(authentication_data.twitch_token)
    if not access_token:
        raise HTTPException(status_code=401, detail="Unable to validate twitch token")

    response.set_cookie(key=AUTH_COOKIE_KEY, value=access_token)

