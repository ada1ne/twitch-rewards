"""Module responsible for generating jwt tokens for system authentication"""

from typing import Optional

import jwt

from twitchrewards.config import settings
from twitchrewards.twitch import TwitchUserName, get_twitch_user_name


def generate_token(twitch_token: str) -> Optional[str]:
    """
    Return the jwt token to authenticate with the API.
    It sends a request to Twitch to check the name to be
    added to the token

    Parameters:
        twitch_token (str): Twitch access token to access its API.

    Returns:
        str: JWT token to authenticate within twitchrewards API.
    """
    get_user_name_result = get_twitch_user_name(twitch_token)

    if isinstance(get_user_name_result, TwitchUserName):
        twitch_user_name = get_user_name_result.name
        return jwt.encode(
            {"twitch_name": twitch_user_name},
            settings.JWT_ENCODING_KEY,
            algorithm=settings.JWT_ENCODING_ALGORITHM,
        )

    return None
