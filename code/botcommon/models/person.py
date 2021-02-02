import datetime

from nonelib import nonelist

from botcommon.bottypes import ChallengeTypeCode
from botcommon.choosers.challengetype import challenge_type_chooser
from botcommon.modelbase import ModelBase
from botcommon.models.challenge import Challenge
from botcommon.models.phrase import Phrase
from botcommon.models.voice import Voice


class Person(ModelBase):

    async def get_new_challenge(self):
        challenge_type = await challenge_type_chooser.async_pick({
            "person_id": self.row.id,
            "person_xp": self.row.xp,
            "n_phrases": self.row.n_phrases,
            "n_voices": self.row.n_voices,
            "n_transcriptions": self.row.n_transcriptions,
            "n_challenges": (self.row.n_phrases + self.row.n_voices + self.row.n_transcriptions),
        })

        if challenge_type == ChallengeTypeCode.CHL_PHR:
            challenge = await Challenge.insert(
                is_active=True,
                created_ts=datetime.datetime.now(),
                person_id=self.row.id,
                type_code="CHL_PHR",
            )
            await self.update(n_phrases=self.row.n_phrases + 1)

        elif challenge_type == ChallengeTypeCode.CHL_VOC:
            phrases = []
            phrases += nonelist([
                await Phrase.choose_fair(self.row.n_prev_success, exclude_phrases=phrases)
            ])
            phrases += nonelist([
                await Phrase.choose_easy(exclude_phrases=phrases)
            ])
            phrases += nonelist([
                await Phrase.choose_random(exclude_phrases=phrases)
            ])

            # assert phrases


            #
            #
            import logging
            logging.debug("  >>>>>>>>>>   phrases = %r", phrases)
            #
            #

            challenge = await Challenge.insert(
                is_active=True,
                created_ts=datetime.datetime.now(),
                person_id=self.row.id,
                type_code="CHL_VOC",
                phrases=[p.row.id for p in phrases],
            )
            await self.update(n_voices=self.row.n_voices + 1)

        elif challenge_type == ChallengeTypeCode.CHL_TRS:
            voices = []
            voices += nonelist([
                await Voice.choose_fair(self.row.n_prev_success, exclude_voices=voices)
            ])
            voices += nonelist([
                await Voice.choose_easy(exclude_voices=voices)
            ])
            voices += nonelist([
                await Voice.choose_random(exclude_voices=voices)
            ])

            # assert voices


            #
            #
            import logging
            logging.debug("  >>>>>>>>>>   voices = %r", voices)
            #
            #

            challenge = await Challenge.insert(
                is_active=True,
                created_ts=datetime.datetime.now(),
                person_id=self.row.id,
                type_code="CHL_TRS",
                voices=[v.row.id for v in voices],
            )
            await self.update(n_transcriptions=self.row.n_transcriptions + 1)

        else:
            challenge = None

        return challenge

        # TODO: pick N- challenges from the type:
        # - xp relevant
        # - simple
        # - random

        pass  # ?
