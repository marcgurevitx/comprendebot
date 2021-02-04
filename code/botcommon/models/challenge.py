from botcommon.executors import (
    PhraseChallenge,
    VoiceChallenge,
    TranscriptionChallenge,
)
from botcommon.modelbase import ModelBase


class Challenge(ModelBase):

    def _get_executor(self):
        if self.row.type_code == 'CHL_PHR':
            challenge_executor = PhraseChallenge(self)
        elif self.row.type_code == 'CHL_VOC':
            challenge_executor = VoiceChallenge(self)
        elif self.row.type_code == 'CHL_TRS':
            challenge_executor = TranscriptionChallenge(self)
        return challenge_executor

    async def start(self):
        challenge_executor = self._get_executor()
        sendable = await challenge_executor.start()
        return sendable
