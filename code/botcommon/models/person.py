import datetime
import logging

from nonelib import nonelist
from psycopg2.extras import Json

from botcommon.bottypes import ChallengeTypeCode
from botcommon.choosers.challengetype import challenge_type_chooser
from botcommon.config import config, calc_ratios
from botcommon.modelbase import ModelBase

logger = logging.getLogger(__name__)


def get_challenge_class():
    from botcommon.models import Challenge
    return Challenge


def get_phrase_class():
    from botcommon.models import Phrase
    return Phrase


def get_voice_class():
    from botcommon.models import Voice
    return Voice


class Person(ModelBase):

    @classmethod
    async def find_or_create(cls, telegram_uid, telegram_info):
        person = await cls.select_one(telegram_uid=telegram_uid)
        if person is None:
            person = await cls.insert(
                is_active=True,
                created_ts=datetime.datetime.now(),
                telegram_uid=telegram_uid,
                telegram_info=telegram_uid,
            )
        return person

    async def get_new_challenge(self):
        chltype = await self._choose_new_challenge_type()
        if chltype == ChallengeTypeCode.CHL_PHR:
            challenge = await self._create_challenge_phrase()
        elif chltype == ChallengeTypeCode.CHL_VOC:
            challenge = await self._create_challenge_voice()
        elif chltype == ChallengeTypeCode.CHL_TRS:
            challenge = await self._create_challenge_transcription()
        else:
            challenge = None
        return challenge

    async def _choose_new_challenge_type(self):
        for _ in range(config.CMPDBOT_CHALLENGE_SEVRAL_TIMEZ):
            challenges_history = self.row.challenges_history
            (
                ratio_phrase,
                ratio_voice,
                ratio_transcription,
            ) = calc_ratios([
                challenges_history["CHL_PHR"],
                challenges_history["CHL_VOC"],
                challenges_history["CHL_TRS"],
            ])
            chltype = await challenge_type_chooser.async_pick({
                "person_id": self.row.id,
                "ratio_phrase": ratio_phrase,
                "ratio_voice": ratio_voice,
                "ratio_transcription": ratio_transcription,
            })

            logger.debug("Next chalenge type [%r]", chltype)

            if chltype == ChallengeTypeCode.CHL_PHR:
                challenges_history["CHL_PHR"] += 1
            elif chltype == ChallengeTypeCode.CHL_VOC:
                challenges_history["CHL_VOC"] += 1
            elif chltype == ChallengeTypeCode.CHL_TRS:
                challenges_history["CHL_TRS"] += 1
            await self.update(challenges_history=Json(challenges_history))

            if chltype == ChallengeTypeCode.CHL_PHR:
                if self.row.xp < config.CMPDBOT_CHALLENGE_MIN_XP_PHRASE:
                    continue
            elif chltype == ChallengeTypeCode.CHL_VOC:
                if self.row.xp < config.CMPDBOT_CHALLENGE_MIN_XP_VOICE:
                    continue

            break

        else:
            chltype = None

        return chltype

    async def _create_challenge_phrase(self):
        Challenge = get_challenge_class()
        return await Challenge.insert(
            is_active=True,
            created_ts=datetime.datetime.now(),
            person_id=self.row.id,
            type_code="CHL_PHR",
        )

    async def _create_challenge_voice(self):
        Phrase = get_phrase_class()
        phrases = []
        phrases += nonelist([
            await Phrase.choose_fair(self, exclude_phrases=phrases)
        ])
        phrases += nonelist([
            await Phrase.choose_easy(self, exclude_phrases=phrases)
        ])
        phrases += nonelist([
            await Phrase.choose_random(self, exclude_phrases=phrases)
        ])

        logger.debug("Phrases for voice challenge [%r]", phrases)

        if phrases:
            Challenge = get_challenge_class()
            challenge = await Challenge.insert(
                is_active=True,
                created_ts=datetime.datetime.now(),
                person_id=self.row.id,
                type_code="CHL_VOC",
                phrases=[p.row.id for p in phrases],
            )
        else:
            challenge = None
        return challenge

    async def _create_challenge_transcription(self):
        Voice = get_voice_class()
        voices = []
        voices += nonelist([
            await Voice.choose_fair(self, exclude_voices=voices)
        ])
        voices += nonelist([
            await Voice.choose_easy(self, exclude_voices=voices)
        ])
        voices += nonelist([
            await Voice.choose_random(self, exclude_voices=voices)
        ])

        logger.debug("Voices for transcription challenge [%r]", voices)

        if voices:
            Challenge = get_challenge_class()
            challenge = await Challenge.insert(
                is_active=True,
                created_ts=datetime.datetime.now(),
                person_id=self.row.id,
                type_code="CHL_TRS",
                voices=[v.row.id for v in voices],
            )
        else:
            challenge = None
        return challenge
