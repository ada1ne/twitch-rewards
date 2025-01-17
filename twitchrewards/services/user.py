from twitchrewards.repository import get_user_by_name, create_user
from twitchrewards.models import User, Pronouns, Title

def ensure_exists(user_name: str):
    if not get_user_by_name(user_name):
        create_user(User(name=user_name, pronouns=Pronouns.UNKNOWN, title=Title.NONE))
