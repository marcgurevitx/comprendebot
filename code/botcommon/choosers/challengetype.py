from goodenough import GoodEnough

from botcommon.bottypes import ChallengeTypeCode
from botcommon.config import config
from botcommon.models.challenge import Challenge
from botcommon.models.phrase import Phrase
from botcommon.models.voice import Voice


async def get_items(request):
    return list(ChallengeTypeCode)


async def check_enough_xp(request, item):
    rv = 1.0
    if item == ChallengeTypeCode.CHL_PHR:
        if request["person_xp"] < config.CMPDBOT_CHALLENGE_MIN_XP_PHRASE:
            rv = 0.0
    elif item == ChallengeTypeCode.CHL_VOC:
        if request["person_xp"] < config.CMPDBOT_CHALLENGE_MIN_XP_VOICE:
            rv = 0.0
    return rv


async def check_exists_source(request, item):
    rv = 1.0
    if item == ChallengeTypeCode.CHL_VOC:
        if await Phrase.count(is_active=True) == 0:
            rv = 0.0
    elif item == ChallengeTypeCode.CHL_TRS:
        if await Voice.count(is_active=True) == 0:
            rv = 0.0
    return rv


async def check_probability(request, item):
    rv = 1.0
    if request["n_challenges"] > 0:

        if item == ChallengeTypeCode.CHL_PHR:
            cfg_ratio = config.CMPDBOT_CHALLENGE_CHANCE_PHRASE / config.CMPDBOT_CHALLENGE_CHANCE_TOTAL
            person_ratio = request["n_phrases"] / request["n_challenges"]
        elif item == ChallengeTypeCode.CHL_VOC:
            cfg_ratio = config.CMPDBOT_CHALLENGE_CHANCE_VOICE / config.CMPDBOT_CHALLENGE_CHANCE_TOTAL
            person_ratio = request["n_voices"] / request["n_challenges"]
        elif item == ChallengeTypeCode.CHL_TRS:
            cfg_ratio = config.CMPDBOT_CHALLENGE_CHANCE_TRANSCRIPTION / config.CMPDBOT_CHALLENGE_CHANCE_TOTAL
            person_ratio = request["n_transcriptions"] / request["n_challenges"]

        if person_ratio > cfg_ratio:
            rv = 0.5

    return rv


async def check_various(request, item):
    
    
    
    return 1.0#?


challenge_type_chooser = GoodEnough(
    get_items=get_items,
    rules=[
        #check_enough_xp,
        #check_exists_source,
        check_probability,
        #check_various,
    ],
)
