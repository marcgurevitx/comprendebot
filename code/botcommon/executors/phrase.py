from botcommon.bottypes import PhraseStates, Sendable, Button, SendableTypeCode, Stickers
from botcommon.helpers import get_start_button

from .baseexecutor import BaseExecutor

DATA_ROOT_KEY = ""


def get_phrase_class():
    from botcommon.models import Phrase
    return Phrase


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
        dict(
            trigger="receive_text",
            source=PhraseStates.PHR_WRK,
            dest=PhraseStates.PHR_WRK,
            after="ask_submission",
        ),
        dict(
            trigger="receive_button_press_on_text",
            source=PhraseStates.PHR_WRK,
            dest=PhraseStates.PHR_END,
            after="save_phrase",
        ),
    ]

    async def explain_challenge(self):
        s = Sendable(
            type=SendableTypeCode.SND_STK,
            value=Stickers.PHR,
            is_reply=False,
            buttons=[],
        )
        self.sendables.append(s)
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] Please, help me improve my database.\nSend me a new <b>phrase</b> in LANGUAGE.\nYou can send many variants but only submit one.\n(Send /comensa if you want to skip.)",
            is_reply=False,
            buttons=[],
        )
        self.sendables.append(s)

    async def ask_submission(self, text, message_id):
        submit_button = Button(text="[TTT] Submit", data=message_id)
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="↑",
            is_reply=True,
            buttons=[submit_button],
        )
        self.sendables.append(s)

    async def save_phrase(self, text, message_id):
        Phrase = get_phrase_class()
        await Phrase.add_from_challenge(text, self.challenge)

        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] Thank you for your help! The phrase was successfully saved.",
            is_reply=False,
            buttons=[get_start_button()],
        )
        self.sendables.append(s)

        await self.challenge.update(
            is_active=False,
        )
