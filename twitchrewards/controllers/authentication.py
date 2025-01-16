"""Contains routes related to authentication"""

from fastapi import APIRouter, HTTPException, status

from twitchrewards.authentication import generate_token
from twitchrewards.controllers.view_models.authentication_data import AuthenticationData

router = APIRouter()


@router.post("/token", status_code=status.HTTP_200_OK)
def authenticate(authentication_data: AuthenticationData):
    """Gets JWT to perform write operations in the API"""
    access_token = generate_token(authentication_data.twitch_token,
                                  authentication_data.twitch_client_id)
    if not access_token:
        raise HTTPException(status_code=401, detail="Unable to validate twitch token")

    return {"access_token": access_token}
