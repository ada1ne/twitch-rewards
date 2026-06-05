from fastapi import APIRouter, HTTPException, status

from pydantic import BaseModel
from twitchrewards.repository import get_trophy_by_id, set_trophy_redeemable

router = APIRouter()


class SetRedeemableBody(BaseModel):
    redeemable: bool


@router.post("/api/{trophy_id}/redeemable", status_code=status.HTTP_200_OK)
def set_redeemable(trophy_id: int, body: SetRedeemableBody):
    """Gets metadata of a user to display in chat"""
    trophy = get_trophy_by_id(trophy_id)
    if not trophy:
        raise HTTPException(status_code=404, detail="Trophy not found")

    set_trophy_redeemable(trophy_id, body.redeemable)
