"""Used to interact with the User entity in the database"""

from typing import Optional

from twitchrewards.models import User
from twitchrewards.repository.database import get_db


def get_by_name(name: str) -> Optional[User]:
    """
    Get a user with a given name.

    Parameters:
        name (str): Name of the user.

    Returns:
        User: User with the corresponding name.
    """
    with get_db() as db:
        return db.query(User).filter_by(name=name).first()
