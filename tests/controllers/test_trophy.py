from typing import Optional

import jwt
import pytest
from fastapi.testclient import TestClient

from twitchrewards.main import app
from twitchrewards.models import EarlyUser
from twitchrewards.repository import get_trophy_by_id, set_trophy_redeemable

client = TestClient(app)


@pytest.mark.parametrize(
    "currently_redeemable,is_redeemable",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_set_redeemable_should_set_redeemable(
    currently_redeemable: bool, is_redeemable: bool
):
    trophy = EarlyUser(currently_redeemable)
    set_trophy_redeemable(trophy.id, currently_redeemable)

    response = client.post(
        f"/trophies/api/{trophy.id}/redeemable", json={"redeemable": is_redeemable}
    )
    assert response.status_code == 200

    updated_trophy = get_trophy_by_id(trophy.id)
    assert updated_trophy != None
    assert updated_trophy.redeemable == is_redeemable


def test_set_redeemable_when_trophy_does_not_exist_should_return_404():
    response = client.post(
        f"/trophies/api/12345/redeemable", json={"redeemable": True}
    )

    assert response.status_code == 404
