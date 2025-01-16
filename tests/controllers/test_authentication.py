"""Tests for the authentication controller"""

from dataclasses import dataclass
from datetime import datetime, timezone

import jwt
from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient

import twitchrewards.authentication.jwt
from twitchrewards.config import settings
from twitchrewards.main import app
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


def test_token_returns_jwt_for_user(monkeypatch: MonkeyPatch):
    """Test if the authentication generates the expected token"""
    twitch_name = "test_name"
    given_twitch_request_is_successful(monkeypatch, twitch_name)

    response = client.post("token", json={"twitch_token": "dummy_token"})

    assert response.status_code == 200
    json = response.json()
    assert "access_token" in json
    access_token = json["access_token"]
    decoded_token = jwt.decode(
        access_token, settings.JWT_ENCODING_KEY, settings.JWT_ENCODING_ALGORITHM
    )
    assert "twitch_name" in decoded_token
    assert decoded_token["twitch_name"] == twitch_name
    assert "exp" in decoded_token
    assert datetime.fromtimestamp(decoded_token["exp"], timezone.utc) > datetime.now(
        timezone.utc
    )


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
        twitchrewards.authentication.jwt,
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
        twitchrewards.authentication.jwt,
        "get_twitch_user_name",
        mock_get_twitch_user_name,
    )

    mock_data.is_twitch_response_successful = False
