from botcommon.bottypes import TranscriptionStates

from .baseexecutor import BaseExecutor


class TranscriptionExecutor(BaseExecutor):
    states = TranscriptionStates
    initial = TranscriptionStates.TRS_CRE
    transitions = [
        dict(
            trigger="start",
            source=TranscriptionStates.TRS_CRE,
            dest=TranscriptionStates.TRS_WRK,
            after="explain_challenge",
        ),
    ]

    async def explain_challenge(self):
        sss = "[TTT] Choose one voice..."  # + 3 buttons
        self.sendables.append(sss)
