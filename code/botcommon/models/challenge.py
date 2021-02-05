from botcommon.executors import (
    PhraseExecutor,
    VoiceExecutor,
    TranscriptionExecutor,
)
from botcommon.modelbase import ModelBase


class Challenge(ModelBase):

    def get_executor(self):
        if self.row.type_code == 'CHL_PHR':
            executor_class = PhraseExecutor
        elif self.row.type_code == 'CHL_VOC':
            executor_class = VoiceExecutor
        elif self.row.type_code == 'CHL_TRS':
            executor_class = TranscriptionExecutor
        executor = executor_class(challenge=self)
        return executor
