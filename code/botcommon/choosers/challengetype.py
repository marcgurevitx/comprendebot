from goodenough import GoodEnough

from botcommon.bottypes import ChallengeTypeCode
from botcommon.config import config


async def get_items(request):
    return list(ChallengeTypeCode)


async def must_drop_phr_if_low_xp(request, item):
    if item != ChallengeTypeCode.CHL_PHR:
        return 1.0
    if request["person_xp"] >= config.CMPDBOT_PHRASE_CHALLENGE_MIN_XP:
        return 1.0
    return 0.0


challenge_type_chooser = GoodEnough(
    get_items=get_items,
    rules=[
        must_drop_phr_if_low_xp,
    ],
)
