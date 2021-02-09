import datetime

from botcommon.choosers.voice import (
    fair_voice_chooser,
    easy_voice_chooser,
    random_voice_chooser,
)
from botcommon.modelbase import ModelBase


class Voice(ModelBase):

    @classmethod
    async def choose_fair(cls, person, exclude_voices):
        return await fair_voice_chooser.async_pick({
            "person_id": person.row.id,
            "person_n_prev_success": person.row.n_prev_success,
            "exclude_voices": [v.row.id for v in exclude_voices],
        })

    @classmethod
    async def choose_easy(cls, person, exclude_voices):
        return await easy_voice_chooser.async_pick({
            "person_id": person.row.id,
            "exclude_voices": [v.row.id for v in exclude_voices],
        })

    @classmethod
    async def choose_random(cls, person, exclude_voices):
        return await random_voice_chooser.async_pick({
            "person_id": person.row.id,
            "exclude_voices": [v.row.id for v in exclude_voices],
        })

    @classmethod
    async def add_from_challenge(cls, phrase_id, phrase_length, voice_key, challenge):
        await cls.insert(
            is_active=True,
            created_ts=datetime.datetime.now(),
            person_id=challenge.row.person_id,
            phrase_id=phrase_id,
            length=phrase_length,
            s3_key=voice_key,
            challenge_id=challenge.row.id,
        )
