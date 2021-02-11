import datetime

from Levenshtein import ratio

from botcommon.bottypes import SimilarPhrase
from botcommon.choosers.phrase import (
    fair_phrase_chooser,
    easy_phrase_chooser,
    random_phrase_chooser,
)
from botcommon.config import config
from botcommon.helpers import normalize_text
from botcommon.models.basemodel import BaseModel


class Phrase(BaseModel):

    @classmethod
    async def choose_fair(cls, person, exclude_phrases):
        return await fair_phrase_chooser.async_pick({
            "person_id": person.row.id,
            "person_n_prev_success": person.row.n_prev_success,
            "exclude_phrases": [p.row.id for p in exclude_phrases],
        })

    @classmethod
    async def choose_easy(cls, person, exclude_phrases):
        return await easy_phrase_chooser.async_pick({
            "person_id": person.row.id,
            "exclude_phrases": [p.row.id for p in exclude_phrases],
        })

    @classmethod
    async def choose_random(cls, person, exclude_phrases):
        return await random_phrase_chooser.async_pick({
            "person_id": person.row.id,
            "exclude_phrases": [p.row.id for p in exclude_phrases],
        })

    @classmethod
    async def find_similar(cls, text):
        normalized_text = normalize_text(text)
        rv = []
        for phrase in await cls.select_all():
            if phrase.row.normalized_text is not None:
                similarity = ratio(normalized_text, phrase.row.normalized_text)
                if similarity >= config.CMPDBOT_SIMILARITY_RATIO:
                    rv.append(SimilarPhrase(phrase=phrase, similarity=similarity))
        return rv, normalized_text

    @classmethod
    async def add_from_cli(cls, text, normalized_text):
        await cls.insert(
            is_active=True,
            created_ts=datetime.datetime.now(),
            original_text=text,
            normalized_text=normalized_text,
        )

    @classmethod
    async def add_from_challenge(cls, text, challenge):
        await cls.insert(
            is_active=True,
            created_ts=datetime.datetime.now(),
            person_id=challenge.row.person_id,
            original_text=text,
            normalized_text=normalize_text(text),
            challenge_id=challenge.row.id,
        )
