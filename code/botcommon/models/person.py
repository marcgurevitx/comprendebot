import datetime
import logging

from nonelib import nonelist
from psycopg2.extras import Json

from botcommon.bottypes import ChallengeTypeCode
from botcommon.choosers.challengetype import challenge_type_chooser
from botcommon.config import config, calc_ratios
from botcommon.models.basemodel import BaseModel

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


class Person(BaseModel):

    async def get_new_challenge(self):
        await self._deactivate_existing_challenges()
        challenge_type = await self._choose_new_challenge_type()
        challenge = await self._create_challenge_by_type(challenge_type)
        return challenge

    async def _deactivate_existing_challenges(self):
        Challenge = get_challenge_class()
        challenges = await Challenge.select_all(
            is_active=True,
            person_id=self.row.id,
        )
        for challenge in challenges:
            await challenge.update(is_active=False)

    async def _choose_new_challenge_type(self):
        for _ in range(config.CHOOSE_SEVRAL_TIMEZ):
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
                if self.row.xp < config.CHOOSE_MIN_XP_PHRASE:
                    continue
            elif chltype == ChallengeTypeCode.CHL_VOC:
                if self.row.xp < config.CHOOSE_MIN_XP_VOICE:
                    continue

            break

        else:
            chltype = None

        return chltype

    async def _create_challenge_by_type(self, challenge_type):
        if challenge_type == ChallengeTypeCode.CHL_PHR:
            challenge = await self._create_challenge_phrase()
        elif challenge_type == ChallengeTypeCode.CHL_VOC:
            challenge = await self._create_challenge_voice()
        elif challenge_type == ChallengeTypeCode.CHL_TRS:
            challenge = await self._create_challenge_transcription()
        else:
            challenge = None
        return challenge

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

    async def get_existing_active_challenge(self):
        Challenge = get_challenge_class()
        return await Challenge.select_one(
            is_active=True,
            person_id=self.row.id,
        )

    @classmethod
    async def increase_xp(cls, xp, person_trs_id, person_voc_id, person_phr_id):
        person_trs = await cls.select_one(id=person_trs_id)
        await person_trs.update(
            xp=person_trs.row.xp + xp,
            n_prev_success=xp,
        )

        person_voc = await Person.select_one(id=person_voc_id)
        if person_voc:
            await person_voc.update(
                xp=person_voc.row.xp + xp,
                generated_xp=person_voc.row.generated_xp + xp,
            )

        if person_phr_id:
            person_phr = await Person.select_one(id=person_phr_id)
            await person_phr.update(
                xp=person_phr.row.xp + xp,
                generated_xp=person_phr.row.generated_xp + xp,
            )

        return person_trs.row.xp
