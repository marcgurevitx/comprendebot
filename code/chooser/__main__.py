from goodenough import GoodEnough

from botcommon.config import config


async def get_items(request):
    return ["YOUR_CHALLENGE_7"]


chooser = GoodEnough(
    get_items=get_items,
)
chooser.serve(port=config.CHOOSER_PORT)
