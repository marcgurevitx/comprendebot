from botcommon.choosers.voice import (
    fair_voice_chooser,
    easy_voice_chooser,
    random_voice_chooser,
)
from botcommon.modelbase import ModelBase


class Voice(ModelBase):

    @classmethod
    async def choose_fair(cls, person_n_prev_success, exclude_voices):
        return await fair_voice_chooser.async_pick({
            "person_n_prev_success": person_n_prev_success,
            "exclude_voices": [v.row.id for v in exclude_voices],
        })

    @classmethod
    async def choose_easy(cls, exclude_voices):
        return await easy_voice_chooser.async_pick({
            "exclude_voices": [v.row.id for v in exclude_voices],
        })

    @classmethod
    async def choose_random(cls, exclude_voices):
        return await random_voice_chooser.async_pick({
            "exclude_voices": [v.row.id for v in exclude_voices],
        })
