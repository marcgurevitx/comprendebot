from botcommon.bottypes import VoiceStates

from .baseexecutor import BaseExecutor


class VoiceExecutor(BaseExecutor):
    states = VoiceStates
    initial = VoiceStates.VOC_CRE
    transitions = [
        dict(
            trigger="start",
            source=VoiceStates.VOC_CRE,
            dest=VoiceStates.VOC_WRK,
            after="explain_challenge",
        ),
    ]

    async def explain_challenge(self):
        sss = "[TTT] Choose one phrase..."  # + 3 buttons
        self.sendables.append(sss)
