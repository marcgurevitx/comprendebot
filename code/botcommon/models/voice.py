import datetime

from botcommon.choosers.voice import (
    fair_voice_chooser,
    easy_voice_chooser,
    random_voice_chooser,
)
from botcommon.config import config
from botcommon.models.basemodel import BaseModel


def get_phrase_class():
    from botcommon.models import Phrase
    return Phrase


def get_person_class():
    from botcommon.models import Person
    return Person


class Voice(BaseModel):

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
        Person = get_person_class()
        person = await Person.select_one(id=challenge.row.person_id)

        await cls.insert(
            is_active=person.row.is_active,
            created_ts=datetime.datetime.now(),
            person_id=challenge.row.person_id,
            phrase_id=phrase_id,
            length=phrase_length,
            s3_key=voice_key,
            challenge_id=challenge.row.id,
        )

    async def get_masked_text(self):
        Phrase = get_phrase_class()
        phrase = await Phrase.select_one(id=self.row.phrase_id)
        words = phrase.row.normalized_text.split()
        masked_words = [
            config.CMPDBOT_MASK * len(w)
            for w
            in words
        ]
        return "\u2003".join(masked_words)
