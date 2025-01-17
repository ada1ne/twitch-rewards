"""Module responsible for generating jwt tokens for system authentication"""

from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from twitchrewards.config import settings
from twitchrewards.services.user import ensure_exists
from twitchrewards.twitch import TwitchUserName, get_access_token, get_twitch_user_name


def authenticate_twitch_user(code: str) -> Optional[str]:
    """
    Return the jwt token to authenticate with the API.
    It sends a request to Twitch to check the name to be
    added to the token

    Parameters:
        code (str): Twitch code to generate access token for the API.

    Returns:
        str: JWT token to authenticate within twitchrewards API.
    """
    twitch_token = get_access_token(code)
    if not twitch_token:
        return None

    get_user_name_result = get_twitch_user_name(twitch_token)

    if isinstance(get_user_name_result, TwitchUserName):
        twitch_user_name = get_user_name_result.name
        ensure_exists(twitch_user_name)
        return jwt.encode(
            {
                "twitch_name": twitch_user_name,
                "exp": datetime.now(timezone.utc)
                + timedelta(0, settings.JWT_EXPIRATION_TIME_IN_SECONDS),
            },
            settings.JWT_ENCODING_KEY,
            algorithm=settings.JWT_ENCODING_ALGORITHM,
        )

    return None


def decode(token: str) -> str:
    """
    Decode JWT token.

    Parameters:
        token (str): Token to decode.

    Returns:
        str: name of the user in Twitch, stored in the token.
    """
    decoded_token = jwt.decode(
        token, settings.JWT_ENCODING_KEY, algorithms=[settings.JWT_ENCODING_ALGORITHM]
    )
    return decoded_token["twitch_name"]
