"""Module to access data for the current session"""

from typing import Annotated, Optional

from fastapi import Header

from twitchrewards.authentication.jwt import decode
from twitchrewards.models import User
from twitchrewards.repository import get_user_by_name


def get_current_user(authorization: Annotated[str, Header()]) -> Optional[User]:
    """
    Get the current user given the token in the Authorization header.

    Parameters:
        authorization (str): Value of the authorization header.

    Returns:
        Optional[User]: The user matching the access token, if any.
    """
    split_token = authorization.split("Bearer ")
    if len(split_token) != 2:
        return None

    token = split_token[1]
    name = decode(token)
    return get_user_by_name(name)
