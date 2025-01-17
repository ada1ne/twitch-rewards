"""For now this is acting as a catch all for the setting page"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse, RedirectResponse

from twitchrewards.models import User
from twitchrewards.services.authentication import get_current_user

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def home(user: Annotated[Optional[User], Depends(get_current_user)]):
    """Allows user to change their personal data"""
    if not user:
        return RedirectResponse("/login")

    return FileResponse("twitchrewards/views/home.html")


@router.get("/login", status_code=status.HTTP_200_OK)
def login():
    """Log in page"""
    return FileResponse("twitchrewards/views/login.html")
