from goodenough import GoodEnough

from botcommon.bottypes import ChallengeTypeCode
from botcommon.config import config
from botcommon.models import (
    get_challenge_class,
    get_phrase_class,
    get_voice_class,
)


async def get_items(request):
    return list(ChallengeTypeCode)


async def ensure_exists_source(request, item):
    rv = 1.0
    if item == ChallengeTypeCode.CHL_VOC:
        Phrase = get_phrase_class()
        if await Phrase.count(is_active=True) < 2:
            rv = 0.0
    elif item == ChallengeTypeCode.CHL_TRS:
        Voice = get_voice_class()
        if await Voice.count(is_active=True) < 2:
            rv = 0.0
    return rv


async def ensure_probability(request, item):
    if item == ChallengeTypeCode.CHL_PHR:
        ratio_diff = config.RATIO_PHRASE - request["ratio_phrase"]
    elif item == ChallengeTypeCode.CHL_VOC:
        ratio_diff = config.RATIO_VOICE - request["ratio_voice"]
    elif item == ChallengeTypeCode.CHL_TRS:
        ratio_diff = config.RATIO_TRANSCRIPTION - request["ratio_transcription"]
    return 0.5 + ratio_diff / 3


async def ensure_various(request, item):
    rv = 1.0
    Challenge = get_challenge_class()
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
            if challenge.row.type_code == 'CHL_PHR':
                rv = 0.5
        elif item == ChallengeTypeCode.CHL_VOC:
            if challenge.row.type_code == 'CHL_VOC':
                rv = 0.5
        elif item == ChallengeTypeCode.CHL_TRS:
            if challenge.row.type_code == 'CHL_TRS':
                rv = 0.5
    return rv


challenge_type_chooser = GoodEnough(
    get_items=get_items,
    rules=[
        ensure_exists_source,
        ensure_probability,
        ensure_various,
    ],
)
