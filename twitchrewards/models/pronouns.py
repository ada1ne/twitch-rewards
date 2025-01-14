"""Pronouns a user may select"""

from enum import Enum


class Pronouns(Enum):
    """Available pronouns. Limit to 3 for this MVP, no support for mixing"""

    UNKNOWN = 0
    HE = 1
    SHE = 2
    THEY = 3
    ALL = 4
