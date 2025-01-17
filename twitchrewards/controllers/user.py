"""Contains routes related to the user"""

from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from twitchrewards.controllers.view_models import (
    UpdatePronounsData,
    UserViewModel,
    get_name_with_title,
)
from twitchrewards.models import Pronouns, User
from twitchrewards.repository import get_user_by_name, update_user
from twitchrewards.services.authentication import get_current_user

router = APIRouter()


@router.get("/{user_name}", status_code=status.HTTP_200_OK)
def fetch_user_metadata(user_name: str):
    """Gets metadata of a user to display in chat"""
    user = get_user_by_name(user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return parse(user)


@router.get("", status_code=status.HTTP_200_OK)
def fetch_current_user(user: Annotated[Optional[User], Depends(get_current_user)]):
    """Fetches the current user base on the current JWT"""
    if not user:
        raise HTTPException(status_code=404, detail="No user authenticated")

    return parse(user)


@router.post("/{user_name}/set-pronouns", status_code=status.HTTP_200_OK)
def update_pronouns(
    user_name: str,
    pronouns: UpdatePronounsData,
    user: Annotated[Optional[User], Depends(get_current_user)],
):
    """Updates the pronouns of a user to display in chat"""
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    if user_name != user.name:
        raise HTTPException(
            status_code=403, detail="Access token does not match target user"
        )

    user.pronouns = pronouns.pronouns
    update_user(user)


def parse_pronouns(pronoun: Pronouns) -> str:
    """
    Return the localized string representation of the pronoun.

    Parameters:
        pronoun (Pronouns): Pronoun to parse.

    Returns:
        str: Localized string representation of the pronoun.
    """
    if pronoun == Pronouns.HE:
        return "ele/dele"
    if pronoun == Pronouns.SHE:
        return "ela/dela"
    if pronoun == Pronouns.THEY:
        return "elu/delu"
    if pronoun == Pronouns.ALL:
        return "todos pronomes"
    return ""


def parse(user: User) -> UserViewModel:
    """
    Return the view model representation of the user. Enums are parsed
    to their string representation.

    Parameters:
        user (User): User to be parsed.

    Returns:
        UserViewModel: Parsed user.
    """
    pronouns = parse_pronouns(user.pronouns)
    display_name = get_name_with_title(user.title, user.name, user.pronouns)
    return UserViewModel(
        display_name=display_name, pronouns=pronouns, pronouns_id=user.pronouns
    )
