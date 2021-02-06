from botcommon.bottypes import PhraseStates, Sendable

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

        s = Sendable(
            type="text",
            value="[TTT] Send me phrase.",
            is_reply=False,
            buttons=[],
        )

        self.sendables.append(s)
