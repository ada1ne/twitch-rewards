"""Orchestration layer for user management"""

from twitchrewards.models import Pronouns, Title, User
from twitchrewards.repository import create_user, get_user_by_name


def ensure_exists(user_name: str):
    """
    Creates a user with a given name, if one does not exist already.

    Parameters:
        user_name (str): Name of the user.
    """
    if not get_user_by_name(user_name):
        create_user(User(name=user_name, pronouns=Pronouns.UNKNOWN, title=Title.NONE))
