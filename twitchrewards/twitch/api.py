from dataclasses import dataclass

@dataclass
class TwitchResponse:
    pass

@dataclass
class TwitchBadResponse(TwitchResponse):
    pass

@dataclass
class TwitchUserName(TwitchResponse):
    name: str


def get_user_name(token: str) -> TwitchResponse:
    pass
