"""Base class for classes using sqlalchemy's ORM"""

from dataclasses import dataclass


@dataclass
class Base(DeclarativeBase):
    """Base class for classes using sqlalchemy's ORM"""
