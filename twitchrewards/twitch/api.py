"""Methods used to interact with Twitch's API"""

from dataclasses import dataclass


@dataclass
class TwitchResponse:
    """Represents a response from the Twitch API"""


@dataclass
class TwitchBadResponse(TwitchResponse):
    """Represents a failed response from Twitch API"""


@dataclass
class TwitchUserName(TwitchResponse):
    """Wraps the username from a successful Twitch API response"""

    name: str


def get_user_name(_: str) -> TwitchResponse:
    """
    Return the Twitch name of the user that owns the given token

    Parameters:
        _ (str): Twitch access token to access its API.

    Returns:
        TwitchResponse: Whether the call succeeded or not, and it's content in case of success.
    """
    return TwitchBadResponse()
