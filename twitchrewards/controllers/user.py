"""Contains routes related to the user's chat metadata"""

from fastapi import APIRouter, HTTPException, status

from twitchrewards.controllers.view_models.titles import get_name_with_title
from twitchrewards.controllers.view_models.user_view_model import UserViewModel
from twitchrewards.models import Pronouns, User
from twitchrewards.repository import get_user_by_name

router = APIRouter()


@router.get("/{user_name}", status_code=status.HTTP_200_OK)
def fetch_user_metadata(user_name: str):
    """Gets metadata of a user to display in chat"""
    user = get_user_by_name(user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return parse(user)


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
    return UserViewModel(display_name=display_name, pronouns=pronouns)
