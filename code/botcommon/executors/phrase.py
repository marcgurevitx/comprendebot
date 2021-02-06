from psycopg2.extras import Json

from botcommon.bottypes import PhraseStates, Sendable, Button, SendableTypeCode
from botcommon.config import config

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
            trigger="receive_edit",
            source=PhraseStates.PHR_WRK,
            dest=PhraseStates.PHR_WRK,
            after="edit_variant",
        ),
        dict(
            trigger="receive_button_press",
            source=PhraseStates.PHR_WRK,
            dest=PhraseStates.PHR_END,
            after="save_phrase",
        ),
    ]

    async def explain_challenge(self):
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] Send me phrase.",
            is_reply=False,
            buttons=[],
        )
        self.sendables.append(s)

    async def ask_submission(self, text, message_id):
        executor_data = self.challenge.row.executor_data
        user_variants = executor_data.setdefault(DATA_ROOT_KEY, {})
        user_variants[str(message_id)] = text
        submit_button = Button(text="[TTT] Submit", data=message_id)
        await self.challenge.update(executor_data=Json(executor_data))
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] Press 'Submit' to submit, or send another one.",
            is_reply=True,
            buttons=[submit_button],
        )
        self.sendables.append(s)

    async def edit_variant(self, text, message_id):
        executor_data = self.challenge.row.executor_data
        user_variants = executor_data[DATA_ROOT_KEY]
        user_variants[str(message_id)] = text
        await self.challenge.update(executor_data=Json(executor_data))

    async def save_phrase(self, message_id):
        executor_data = self.challenge.row.executor_data
        user_variants = executor_data[DATA_ROOT_KEY]
        text = user_variants[str(message_id)]

        Phrase = get_phrase_class()
        await Phrase.add_from_challenge(text, self.challenge)

        await self.challenge.update(
            is_active=False,
        )

        restart_button = Button(
            text="[TTT] Start new challenge",
            data=config.CMPDBOT_CONST_START,
        )
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] Thank you. The phrase is successfully saved.",
            is_reply=False,
            buttons=[restart_button],
        )
        self.sendables.append(s)
