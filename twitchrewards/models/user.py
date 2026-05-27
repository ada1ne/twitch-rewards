"""Contains the representation of a Twitch user"""

from dataclasses import dataclass

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped

from twitchrewards.models.base_db_model import Base
from twitchrewards.models.pronouns import Pronouns
from twitchrewards.models.sqlalchemy_enum_type import IntEnum
from twitchrewards.models.titles import Title
from twitchrewards.models.trophy import Trophy
from twitchrewards.models.user_trophy_association import _users_trophies_table


@dataclass
class User(Base):
    """
    Store data for a Twitch user. User are identified by name.
    Changing the name on Twitch requires an update here.
    """

    __tablename__ = "Users"

    id: int = Column(Integer, name="Id", primary_key=True)
    name: str = Column(String, name="Name")
    pronouns: Pronouns = Column(IntEnum(Pronouns), name="Pronouns")
    title: Title = Column(IntEnum(Title), name="Title")
    children: Mapped[List[Trophy]] = relationship(secondary=_users_trophies_table)
