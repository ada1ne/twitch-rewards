"""Contains routes related to authentication"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, Response

from twitchrewards.controllers.view_models import AuthenticationData
from twitchrewards.services.authentication import AUTH_COOKIE_KEY, generate_token

router = APIRouter()


@router.get("/token")
def handle_twitch_redirect():
    """Sends user to a temporary page where we will post the Twitch token"""
    return FileResponse("twitchrewards/views/authenticate.html")


@router.post("/token", status_code=status.HTTP_200_OK)
def authenticate(authentication_data: AuthenticationData, response: Response):
    """Gets JWT to perform write operations in the API"""
    access_token = generate_token(authentication_data.code)
    if not access_token:
        raise HTTPException(status_code=401, detail="Unable to validate twitch token")

    response.set_cookie(key=AUTH_COOKIE_KEY, value=f"Bearer {access_token}")
