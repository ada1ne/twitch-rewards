"""Used to interact with the User entity in the database"""

from typing import Optional

from sqlalchemy import update

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

def update_user(user: User):
    """
    Update a user in the DB to match the given data.

    Parameters:
        user (User): User to update. It'll update data where using the Id for filtering.
    """
    stmt = (
        update(User)
        .where(User.id == user.id)  # type: ignore
        .values(pronouns=user.pronouns, title=user.title)
    )
    with get_db() as db:
        db.execute(stmt)
        db.commit()

def create_user(user: User):
    """
    Adds a user to the DB.

    Parameters:
        user (User): User to be added.
    """
    with get_db() as db:
        db.add(user)
        db.commit()
