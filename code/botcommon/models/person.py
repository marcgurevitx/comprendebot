import datetime

from botcommon.choosers.challengetype import challenge_type_chooser
from botcommon.modelbase import ModelBase
from botcommon.models.challenge import Challenge
from botcommon.models.phrase import Phrase


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

            challenge = Challenge.insert(
                is_active=True,
                created_ts=datetime.datetime.now(),
                person_id=self.row.id,
                type_code="CHL_PHR",
            )

            self.update(n_phrases=self.row.n_phrases + 1)

        elif challenge_type == ChallengeTypeCode.CHL_VOC:

            phrase_1 = await Phrase.choose_fair([], self.row.n_prev_success)
            phrase_2 = await Phrase.choose_easy([phrase_1.row.id])
            phrase_3 = await Phrase.choose_random([phrase_1.row.id, phrase_2.row.id])
            
            #
            #
            import logging
            logging.debug("  >>>>>>>>>>   phrase_1 = %r", phrase_1)
            logging.debug("  >>>>>>>>>>   phrase_2 = %r", phrase_2)
            logging.debug("  >>>>>>>>>>   phrase_3 = %r", phrase_3)
            #
            #
            
            challenge = Challenge.insert(
                is_active=True,
                created_ts=datetime.datetime.now(),
                person_id=self.row.id,
                type_code="CHL_VOC",
            )

            self.update(n_voices=self.row.n_voices + 1)

        elif challenge_type == ChallengeTypeCode.CHL_TRS:

            voice_1 = ?
            voice_2 = ?
            voice_3 = ?
            
            
            
            
            ?

            self.update(n_transcriptions=self.row.n_transcriptions + 1)

        else:
            challenge = None

        return challenge

        # TODO: pick N- challenges from the type:
        # - xp relevant
        # - simple
        # - random

        pass  # ?
