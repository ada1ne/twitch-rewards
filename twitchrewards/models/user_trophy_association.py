"""SQLAlchemy functions to define the relationship between users and trophies"""

_users_trophies_table = Table(
    "UsersTrophies",
    Base.metadata,
    Column("UserId", ForeignKey("Users.Id")),
    Column("TrophyId", ForeignKey("Trophies.Id")),
)
