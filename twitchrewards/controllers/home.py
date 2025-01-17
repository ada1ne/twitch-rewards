"""For now this is acting as a catch all for the setting page"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from twitchrewards.config import settings
from twitchrewards.models import User
from twitchrewards.services.authentication import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="twitchrewards/views")


@router.get("/", status_code=status.HTTP_200_OK)
def home(user: Annotated[Optional[User], Depends(get_current_user)]):
    """Allows user to change their personal data"""
    if not user:
        return RedirectResponse("/login")

    return FileResponse("twitchrewards/views/home.html")


@router.get("/login", status_code=status.HTTP_200_OK)
def login(request: Request):
    """Log in page"""
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "redirect_uri": f"{settings.APP_HOST}:{settings.APP_PORT}",
            "client_id": settings.TWITCH_APP_CLIENT_ID,
        },
    )
