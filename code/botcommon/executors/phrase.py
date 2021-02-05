from botcommon.bottypes import PhraseStates

from .baseexecutor import BaseExecutor


class PhraseExecutor(BaseExecutor):
    states = PhraseStates
    initial = PhraseStates.PHR_CRE
    transitions = [
        dict(
            trigger="start",
            source=PhraseStates.PHR_CRE,
            dest=PhraseStates.PHR_WRK,
            after="explain_challenge",
        ),
    ]

    async def explain_challenge(self):
        sss = "[TTT] Send me phrase."
        self.sendables.append(sss)
