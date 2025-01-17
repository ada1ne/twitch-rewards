"""Tests for the authentication controller"""

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

import jwt
from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient

import twitchrewards.services.authentication.jwt
from twitchrewards.config import settings
from twitchrewards.main import app
from twitchrewards.repository import get_user_by_name
from twitchrewards.services.authentication import AUTH_COOKIE_KEY
from twitchrewards.twitch import TwitchBadResponse, TwitchResponse, TwitchUserName


@dataclass
class MockGetTwitchUserNameSettings:
    """Data used for the mocked Twitch API call"""

    is_twitch_response_successful = True
    twitch_user_name = "test"


client = TestClient(app)
mock_data = MockGetTwitchUserNameSettings()


def mock_get_twitch_user_name(_: str) -> TwitchResponse:
    """
    Mock the Twitch API call. Use MockGetTwitchUserNameSettings
    to customize the returned values.
    """
    if not mock_data.is_twitch_response_successful:
        return TwitchBadResponse()

    return TwitchUserName(mock_data.twitch_user_name)


def test_token_sets_jwt_for_user(monkeypatch: MonkeyPatch):
    """Test if the authentication generates the expected token"""
    twitch_name = "test_name"
    given_twitch_request_is_successful(monkeypatch, twitch_name)

    response = client.post("token", json={"twitch_token": "dummy_token"})

    assert response.status_code == 200

    assert AUTH_COOKIE_KEY in client.cookies
    cookie = str(client.cookies[AUTH_COOKIE_KEY])[1:-1]
    assert cookie.startswith("Bearer ")
    access_token = cookie.split("Bearer ")[1]
    decoded_token = jwt.decode(
        access_token, settings.JWT_ENCODING_KEY, settings.JWT_ENCODING_ALGORITHM
    )
    assert "twitch_name" in decoded_token
    assert decoded_token["twitch_name"] == twitch_name
    assert "exp" in decoded_token
    assert datetime.fromtimestamp(decoded_token["exp"], timezone.utc) > datetime.now(
        timezone.utc
    )


def test_if_user_does_not_exist_should_create_user(monkeypatch: MonkeyPatch):
    """Test if a new user is being created when token is valid but there is no user"""
    twitch_name = str(uuid.uuid4())
    given_twitch_request_is_successful(monkeypatch, twitch_name)

    response = client.post("token", json={"twitch_token": "dummy_token"})

    assert response.status_code == 200

    user = get_user_by_name(twitch_name)
    assert user is not None
    assert user.name == twitch_name


def test_token_returns_unauthorized_if_authentication_failed(monkeypatch: MonkeyPatch):
    """Test if the route returns 401 if the Twitch API call fails"""
    given_twitch_request_failed(monkeypatch)

    response = client.post("token", json={"twitch_token": "dummy_token"})

    assert response.status_code == 401


def given_twitch_request_is_successful(monkeypatch: MonkeyPatch, twitch_name: str):
    """
    Set Twitch API mock to return a successful request.

    Parameters:
        monkeypatch (MonkeyPatch): helper class to set up the mock.
        twitch_name (str): the name of the user in Twitch.
    """
    monkeypatch.setattr(
        twitchrewards.services.authentication.jwt,
        "get_twitch_user_name",
        mock_get_twitch_user_name,
    )

    mock_data.is_twitch_response_successful = True
    mock_data.twitch_user_name = twitch_name


def given_twitch_request_failed(monkeypatch: MonkeyPatch):
    """
    Set Twitch API mock to return a bad request.

    Parameters:
        monkeypatch (MonkeyPatch): helper class to set up the mock.
    """
    monkeypatch.setattr(
        twitchrewards.services.authentication.jwt,
        "get_twitch_user_name",
        mock_get_twitch_user_name,
    )

    mock_data.is_twitch_response_successful = False
