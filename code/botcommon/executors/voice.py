from botcommon.bottypes import VoiceStates

from botcommon.bottypes import Sendable, Button, SendableTypeCode

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
        phrases = await self.challenge.get_phrases()
        buttons = [
            Button(text=p.row.original_text, data=p.row.id)
            for p
            in phrases
        ]
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] Choose phrase.",
            is_reply=False,
            buttons=buttons,
        )
        self.sendables.append(s)
