"""Module to access data for the current session"""

from typing import Annotated, Optional

import jwt
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
    if not authorization.startswith("Bearer "):
        return None

    split_token = authorization.split("Bearer ")
    token = split_token[1]
    try:
        name = decode(token)
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return None

    return get_user_by_name(name)
