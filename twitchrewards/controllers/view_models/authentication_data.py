"""Request body for the authentication endpoint"""

from dataclasses import dataclass


@dataclass
class AuthenticationData:
    """Wraps the data required for authenticating a user"""

    twitch_token: str
