import contextlib

from botcommon.executors import (
    PhraseExecutor,
    VoiceExecutor,
    TranscriptionExecutor,
)
from botcommon.modelbase import ModelBase


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
        try:
            yield executor
        finally:
            await executor.save_state()
