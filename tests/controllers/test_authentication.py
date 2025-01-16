import twitchrewards.twitch
import jwt
from fastapi.testclient import TestClient
from twitchrewards.main import app
from twitchrewards.twitch import TwitchUserName, TwitchResponse, TwitchBadResponse
from _pytest.monkeypatch import MonkeyPatch
from twitchrewards.config import settings

client = TestClient(app)


is_twitch_response_successful = True
twitch_user_name = "test"

def mock_get_twitch_user_name() -> TwitchResponse:
    if not is_twitch_response_successful:
        return TwitchBadResponse()

    return TwitchUserName(twitch_user_name)

def test_token_returns_jwt_for_user(monkeypatch: MonkeyPatch):
    twitch_name = "test_name"
    given_twitch_request_is_successful(monkeypatch, twitch_name)

    response = client.post("token", json={"twitch_token": "dummy_token"})

    assert response.status_code == 200
    json = response.json()
    assert "access_token" in json
    access_token = json["access_token"]
    decoded_token = jwt.decode(access_token, settings.JWT_ENCODING_KEY, settings.JWT_ENCODING_ALGORITHM)
    assert "twitch_name" in decoded_token
    assert decoded_token["twitch_name"] == twitch_name

def test_token_returns_unauthorized_if_authentication_failed(monkeypatch: MonkeyPatch):
    given_twitch_request_failed(monkeypatch)

    response = client.post("token", json={"twitch_token": "dummy_token"})

    assert response.status_code == 401

def given_twitch_request_is_successful(monkeypatch: MonkeyPatch, twitch_name: str):
    global is_twitch_response_successful, twitch_user_name

    monkeypatch.setattr(twitchrewards.twitch, "get_twitch_user_name", mock_get_twitch_user_name)

    is_twitch_response_successful = True
    twitch_user_name = twitch_name

def given_twitch_request_failed(monkeypatch: MonkeyPatch):
    global is_twitch_response_successful

    monkeypatch.setattr(twitchrewards.twitch, "get_twitch_user_name", mock_get_twitch_user_name)

    is_twitch_response_successful = False
