from goodenough import GoodEnough

from botcommon.bottypes import ChallengeTypeCode
from botcommon.config import config
from botcommon.db import get_pg_cursor


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
    from botcommon.models.phrase import Phrase
    from botcommon.models.voice import Voice

    rv = 1.0
    if item == ChallengeTypeCode.CHL_VOC:
        if await Phrase.count(is_active=True) == 0:
            rv = 0.0
    elif item == ChallengeTypeCode.CHL_TRS:
        if await Voice.count(is_active=True) == 0:
            rv = 0.0
    return rv


async def check_probability(request, item):
    rv = 0.5
    if request["n_challenges"] > 0:
        if item == ChallengeTypeCode.CHL_PHR:
            ratio_diff = config.RATIO_PHRASE - request["n_phrases"] / request["n_challenges"]
        elif item == ChallengeTypeCode.CHL_VOC:
            ratio_diff = config.RATIO_VOICE - request["n_voices"] / request["n_challenges"]
        elif item == ChallengeTypeCode.CHL_TRS:
            ratio_diff = config.RATIO_TRANSCRIPTION - request["n_transcriptions"] / request["n_challenges"]
        rv += ratio_diff / 2
    return rv


async def check_various(request, item):
    from botcommon.models.challenge import Challenge

    rv = 1.0
    challenge = await Challenge.select_sql_one(
        f"""
            SELECT
                *
            FROM
                {Challenge.get_table_name()}
            WHERE
                person_id = %(person_id)s
            ORDER BY
                created_ts DESC
            LIMIT 1
            ;
        """,
        person_id=request["person_id"],
    )
    if challenge is not None:
        if item == ChallengeTypeCode.CHL_PHR:
            if challenge.type_code == 'CHL_PHR':
                rv = 0.5
        elif item == ChallengeTypeCode.CHL_VOC:
            if challenge.type_code == 'CHL_VOC':
                rv = 0.5
        elif item == ChallengeTypeCode.CHL_TRS:
            if challenge.type_code == 'CHL_TRS':
                rv = 0.5
    return rv


challenge_type_chooser = GoodEnough(
    get_items=get_items,
    rules=[
        #check_enough_xp,
        #check_exists_source,
        check_probability,
        #check_various,
    ],
)
