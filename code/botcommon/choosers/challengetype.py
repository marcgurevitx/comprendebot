from goodenough import GoodEnough

from botcommon.bottypes import ChallengeTypeCode


async def get_items(request):
    return [t.name for t in ChallengeTypeCode]


challenge_type_chooser = GoodEnough(
    get_items=get_items,
)
