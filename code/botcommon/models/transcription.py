import datetime

from botcommon.modelbase import ModelBase


class Transcription(ModelBase):

    @classmethod
    async def add_from_challenge(cls, voice_id, text, distance, challenge):
        await cls.insert(
            is_active=True,
            created_ts=datetime.datetime.now(),
            person_id=challenge.row.person_id,
            voice_id=voice_id,
            user_text=text,
            distance=distance,
            challenge_id=challenge.row.id,
        )
