"""Tests for the user controller"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
import pytest
from fastapi.testclient import TestClient

from twitchrewards.config import settings
from twitchrewards.main import app
from twitchrewards.models import Pronouns, Title, User
from twitchrewards.repository import get_user_by_name
from twitchrewards.repository.database import get_db

client = TestClient(app)


@pytest.mark.parametrize(
    "pronouns,expected_description",
    [
        (Pronouns.UNKNOWN, ""),
        (Pronouns.HE, "ele/dele"),
        (Pronouns.SHE, "ela/dela"),
        (Pronouns.THEY, "elu/delu"),
        (Pronouns.ALL, "todos pronomes"),
    ],
)
def test_should_return_pronouns(pronouns: Pronouns, expected_description: str):
    """Test if pronouns are returned correctly"""
    user_name = str(uuid.uuid4())
    given_user(user_name, pronouns)

    response = client.get(f"/users/{user_name}")
    assert response.status_code == 200

    user = response.json()
    assert user["pronouns"] == expected_description


def test_when_user_does_not_exists_should_return_404():
    """Test if pronouns are returned correctly"""
    user_name = str(uuid.uuid4())

    response = client.get(f"/users/{user_name}")

    assert response.status_code == 404


def test_when_user_does_not_have_title_should_return_name():
    """Test if the display name is returned when user has no title set"""
    user_name = str(uuid.uuid4())
    given_user(user_name)

    response = client.get(f"/users/{user_name}")
    assert response.status_code == 200

    user = response.json()
    assert user["display_name"] == user_name


@pytest.mark.parametrize(
    "pronouns",
    [
        Pronouns.UNKNOWN,
        Pronouns.HE,
        Pronouns.SHE,
        Pronouns.THEY,
        Pronouns.ALL,
    ],
)
def test_when_user_has_streamer_title_should_return_name(pronouns: Pronouns):
    """Test if pronouns are returned correctly"""
    user_name = str(uuid.uuid4())
    given_user(user_name, pronouns, title=Title.STREAMER)

    response = client.get(f"/users/{user_name}")
    assert response.status_code == 200

    user = response.json()
    assert user["display_name"] == f"Streamer {user_name}"


def test_when_updating_pronouns_and_jwt_token_is_valid_update_pronouns():
    """Test if API returns 401 when token is invalid"""
    user_name = str(uuid.uuid4())
    given_user(user_name, Pronouns.UNKNOWN)
    token = given_valid_token(user_name)

    response = client.post(
        f"/users/{user_name}/set-pronouns",
        headers={"Authorization": f"Bearer {token}"},
        json={"pronouns": 2},
    )
    assert response.status_code == 200

    user = get_user_by_name(user_name)
    assert user.pronouns == Pronouns.SHE


def test_when_updating_pronouns_and_jwt_token_is_invalid_returns_unauthorized():
    """Test if API returns 401 when token is invalid"""
    user_name = str(uuid.uuid4())
    given_user(user_name, Pronouns.UNKNOWN)
    token = "foo"

    response = client.post(
        f"/users/{user_name}/set-pronouns",
        headers={"Authorization": f"Bearer {token}"},
        json={"pronouns": 2},
    )
    assert response.status_code == 401


def test_when_updating_pronouns_and_jwt_token_is_expired_returns_unauthorized():
    """Test if API returns 401 when token is expired"""
    user_name = str(uuid.uuid4())
    given_user(user_name, Pronouns.UNKNOWN)
    token_expire_date = datetime.now(timezone.utc) - timedelta(1)
    token = given_valid_token(user_name, expires_at=token_expire_date)

    response = client.post(
        f"/users/{user_name}/set-pronouns",
        headers={"Authorization": f"Bearer {token}"},
        json={"pronouns": 2},
    )
    assert response.status_code == 401


def given_user(
    name: str, pronouns: Pronouns = Pronouns.THEY, title: Title = Title.NONE
):
    """Insert a new user in the database."""
    with get_db() as db:
        user = User(name=name, pronouns=pronouns, title=title)
        db.add(user)
        db.commit()


def given_valid_token(twitch_name: str, expires_at: Optional[datetime] = None):
    """Encodes a valid JWT token to authenticate in the application."""
    token_data = {
        "twitch_name": twitch_name,
    }
    if expires_at:
        token_data["exp"] = expires_at

    return jwt.encode(
        token_data,
        settings.JWT_ENCODING_KEY,
        algorithm=settings.JWT_ENCODING_ALGORITHM,
    )
