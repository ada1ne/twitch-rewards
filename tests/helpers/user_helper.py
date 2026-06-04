from twitchrewards.models import Pronouns, Title, User
from twitchrewards.repository import create_user, get_user_by_name


def given_user(
    name: str,
    pronouns: Pronouns = Pronouns.THEY,
    title: Title = Title.NONE,
    profile_image_url: str = "http://foo.test",
) -> User:
    """Insert a new user in the database."""

    create_user(
        User(
            name=name,
            pronouns=pronouns,
            title=title,
            profile_image_url=profile_image_url,
        )
    )
    return get_user_by_name(name)  # type: ignore
