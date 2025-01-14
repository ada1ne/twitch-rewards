"""User representation returned by the API"""

from dataclasses import dataclass


@dataclass
class UserViewModel:
    """Just like the User modal but with enums already parsed to string"""

    display_name: str
    pronouns: str
