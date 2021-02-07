import contextlib

from botcommon.executors import (
    PhraseExecutor,
    VoiceExecutor,
    TranscriptionExecutor,
)
from botcommon.modelbase import ModelBase


def get_phrase_class():
    from botcommon.models import Phrase
    return Phrase


class Challenge(ModelBase):

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
