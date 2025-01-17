"""Request body for the token creation endpoint"""

from dataclasses import dataclass

@dataclass
class AuthenticationData:
    """Wraps the data required for validating the user"""
    twitch_token: str
