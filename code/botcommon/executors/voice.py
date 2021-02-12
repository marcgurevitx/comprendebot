from psycopg2.extras import Json

from botcommon.bottypes import VoiceStates, Sendable, Button, SendableTypeCode, Stickers
from botcommon.helpers import get_start_button
from botcommon.s3 import save_binary

from .baseexecutor import BaseExecutor


def get_phrase_class():
    from botcommon.models import Phrase
    return Phrase


def get_voice_class():
    from botcommon.models import Voice
    return Voice


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
            trigger="receive_button_press_on_nothing",
            source=VoiceStates.VOC_WRK,
            dest=VoiceStates.VOC_WRK,
            after="ask_voice",
        ),
        dict(
            trigger="receive_voice",
            source=VoiceStates.VOC_WRK,
            dest=VoiceStates.VOC_WRK,
            after="ask_submission",
        ),
        dict(
            trigger="receive_button_press_on_voice",
            source=VoiceStates.VOC_WRK,
            dest=VoiceStates.VOC_END,
            after="save_voice",
        ),
    ]

    async def explain_challenge(self):
        s = Sendable(
            type=SendableTypeCode.SND_STK,
            value=Stickers.VOC,
            is_reply=False,
            buttons=[],
        )
        self.sendables.append(s)

        phrases = await self.challenge.get_phrases()
        buttons = [
            Button(text=p.row.original_text, data=p.row.id)
            for p
            in phrases
        ]
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] This challenge is about reading out loud.\nIt will gain you points when others transcribe your recording.\nPick phrase and send me a <b>voice</b>.\nYou can send many variants but only submit one.\n(Send /comensa if you want to skip.)",
            is_reply=False,
            buttons=buttons,
        )
        self.sendables.append(s)

    async def ask_voice(self, callback_data):
        phrase_id = int(callback_data)

        Phrase = get_phrase_class()
        phrase = await Phrase.select_one(id=phrase_id)

        executor_data = self.challenge.row.executor_data
        executor_data["phrase_id"] = phrase_id
        executor_data["phrase_length"] = len(phrase.row.normalized_text)
        await self.challenge.update(executor_data=Json(executor_data))

        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value=f"[TTT] Now send voice recording for <b>{phrase.row.original_text!r}</b>.\nYou can send many variants but only submit one.\nIf you changed your mind, pick another phrase.",
            is_reply=False,
            buttons=[],
        )
        self.sendables.append(s)

    async def ask_submission(self, voice, message_id):
        submit_button = Button(text="[TTT] Submit", data=message_id)
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="↑",
            is_reply=True,
            buttons=[submit_button],
        )
        self.sendables.append(s)

    async def save_voice(self, voice_key, voice_bytes, callback_data):
        await save_binary(voice_key, voice_bytes)

        executor_data = self.challenge.row.executor_data
        phrase_id = executor_data["phrase_id"]
        phrase_length = executor_data["phrase_length"]

        Voice = get_voice_class()
        await Voice.add_from_challenge(phrase_id, phrase_length, voice_key, self.challenge)

        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] Thank you very much! The voice was successfully saved and soon will become available for others.",
            is_reply=False,
            buttons=[get_start_button()],
        )
        self.sendables.append(s)

        await self.challenge.update(
            is_active=False,
        )
