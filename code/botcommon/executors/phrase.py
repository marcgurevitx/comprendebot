from psycopg2.extras import Json

from botcommon.bottypes import PhraseStates, Sendable, Button

from .baseexecutor import BaseExecutor

DATA_ROOT_KEY = ""


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
    ]

    async def explain_challenge(self):
        s = Sendable(
            type="text",
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
            type="text",
            value="[TTT] Press 'Submit' to submit this phrase, or send another one.",
            is_reply=True,
            buttons=[submit_button],
        )
        self.sendables.append(s)

    async def edit_variant(self, text, message_id):
        executor_data = self.challenge.row.executor_data
        user_variants = executor_data[DATA_ROOT_KEY]
        user_variants[str(message_id)] = text
        await self.challenge.update(executor_data=Json(executor_data))
