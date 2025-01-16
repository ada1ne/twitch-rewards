"""Methods used to interact with Twitch's API"""

from dataclasses import dataclass
import requests

TWITCH_GET_USER_URL = 'https://api.twitch.tv/helix/users'

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


def get_user_name(twitch_token: str, twitch_client_id: str) -> TwitchResponse:
    """
    Return the Twitch name of the user that owns the given token

    Parameters:
        twitch_token (str): Twitch access token to access its API.
        twitch_client_id (str): Which Twitch application to make the request in behalf of.

    Returns:
        TwitchResponse: Whether the call succeeded or not, and it's content in case of success.
    """
    r = requests.get(TWITCH_GET_USER_URL, headers= {
        "Authorization": f"Bearer {twitch_token}",
        "Client-Id": twitch_client_id,
    })
    if r.status_code != 200:
        return TwitchBadResponse()

    name = r.json()['data'][0]['display_name']
    return TwitchUserName(name)