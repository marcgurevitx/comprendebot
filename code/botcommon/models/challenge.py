import contextlib

from botcommon.executors import (
    PhraseExecutor,
    VoiceExecutor,
    TranscriptionExecutor,
)
from botcommon.models.basemodel import BaseModel


def get_phrase_class():
    from botcommon.models import Phrase
    return Phrase


def get_voice_class():
    from botcommon.models import Voice
    return Voice


class Challenge(BaseModel):

    def _get_executor_class(self):
        if self.row.type_code == 'CHL_PHR':
            executor_class = PhraseExecutor
        elif self.row.type_code == 'CHL_VOC':
            executor_class = VoiceExecutor
        elif self.row.type_code == 'CHL_TRS':
            executor_class = TranscriptionExecutor
        return executor_class

    @contextlib.asynccontextmanager
    async def get_executor(self):
        executor_class = self._get_executor_class()
        executor = executor_class(challenge=self)
        yield executor
        await executor.save_state()

    async def get_phrases(self):
        if not self.row.phrases:
            rv = []
        else:
            Phrase = get_phrase_class()
            rv = await Phrase.select_sql_all(
                f"""
                    SELECT
                        *
                    FROM
                        {Phrase.get_table_name()}
                    WHERE
                        id in %(phrase_ids)s
                    ;
                """,
                phrase_ids=tuple(self.row.phrases),
            )
        return rv

    async def get_voices(self):
        if not self.row.voices:
            rv = []
        else:
            Voice = get_voice_class()
            rv = await Voice.select_sql_all(
                f"""
                    SELECT
                        *
                    FROM
                        {Voice.get_table_name()}
                    WHERE
                        id in %(voice_ids)s
                    ;
                """,
                voice_ids=tuple(self.row.voices),
            )
        return rv
