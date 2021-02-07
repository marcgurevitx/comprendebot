from psycopg2.extras import Json

from botcommon.bottypes import VoiceStates, Sendable, Button, SendableTypeCode

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
        dict(
            trigger="receive_button_press",
            source=VoiceStates.VOC_WRK,
            dest=VoiceStates.VOC_WRK,
            conditions=["is_phrase_pressed"],
            after="ask_voice",
        ),
        
        
        # ...
        
        
        #dict(
        #    trigger="receive_button_press",
        #    source=PhraseStates.VOC_WRK,
        #    dest=PhraseStates.VOC_END,
        #    conditions=["is_submit_pressed"],
        #    after="save_voice",
        #),
    ]

    async def explain_challenge(self):
        phrases = await self.challenge.get_phrases()
        buttons = [
            Button(text=p.row.original_text, data=f"p:{p.row.id}")
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

    async def is_phrase_pressed(self, callback_data):
        return callback_data.startswith("p:")

    async def ask_voice(self, callback_data):
        phrase_id = int(callback_data[2:])

        executor_data = self.challenge.row.executor_data
        executor_data["phrase_id"] = phrase_id
        await self.challenge.update(executor_data=Json(executor_data))

        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] Now send voice recording.",
            is_reply=False,
            buttons=[],
        )
        self.sendables.append(s)
