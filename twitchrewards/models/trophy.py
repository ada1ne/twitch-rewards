"""Contains the representation of a Trophy"""

from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from twitchrewards.models.base_db_model import Base


@dataclass
class Trophy(Base):
    """
    Store data for a Trophy. A Trophy is a reward a user may claim.
    """

    __tablename__ = "Trophies"

    id: int = Column(Integer, name="Id", primary_key=True)
    name: str = Column(String, name="Name")
    image_url: str = Column(String, name="ImageUrl")
