from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import BaseModel

from twitchrewards.models import User
from twitchrewards.repository import add_trophy, get_trophy_by_id, set_trophy_redeemable
from twitchrewards.services.authentication import get_current_user

router = APIRouter()


class SetRedeemableBody(BaseModel):
    redeemable: bool


@router.post("/api/{trophy_id}/redeemable", status_code=status.HTTP_200_OK)
def set_redeemable(trophy_id: int, body: SetRedeemableBody):
    trophy = get_trophy_by_id(trophy_id)
    if not trophy:
        raise HTTPException(status_code=404, detail="Trophy not found")

    set_trophy_redeemable(trophy_id, body.redeemable)


@router.post("/api/{trophy_id}/redeem", status_code=status.HTTP_200_OK)
def redeem_trophy(
    trophy_id: int, user: Annotated[Optional[User], Depends(get_current_user)]
):
    if not user:
        raise HTTPException(status_code=404, detail="No user authenticated")

    trophy = get_trophy_by_id(trophy_id)
    if not trophy:
        raise HTTPException(status_code=404, detail="Trophy not found")

    if not trophy.redeemable:
        raise HTTPException(status_code=403, detail="Trophy is no longer redeemable")

    add_trophy(user, trophy)
