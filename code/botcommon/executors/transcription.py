from psycopg2.extras import Json

from botcommon.bottypes import TranscriptionStates, Sendable, Button, SendableTypeCode
from botcommon.config import config
from botcommon.helpers import get_distance, get_start_button
from botcommon.s3 import retrieve_binary

from .baseexecutor import BaseExecutor


def get_person_class():
    from botcommon.models import Person
    return Person


def get_phrase_class():
    from botcommon.models import Phrase
    return Phrase


def get_voice_class():
    from botcommon.models import Voice
    return Voice


def get_transcription_class():
    from botcommon.models import Transcription
    return Transcription


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
        dict(
            trigger="receive_button_press_on_nothing",
            source=TranscriptionStates.TRS_WRK,
            dest=TranscriptionStates.TRS_WRK,
            after="ask_transcription",
        ),
        dict(
            trigger="receive_text",
            source=TranscriptionStates.TRS_WRK,
            dest=TranscriptionStates.TRS_WRK,
            after="ask_submission",
        ),
        dict(
            trigger="receive_button_press_on_text",
            source=TranscriptionStates.TRS_WRK,
            dest=TranscriptionStates.TRS_END,
            after="save_transcription",
        ),
    ]

    async def explain_challenge(self):
        voices = await self.challenge.get_voices()
        buttons = [
            Button(text=f"*** ({v.row.length})", data=v.row.id)
            for v
            in voices
        ]
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] Choose voice.",
            is_reply=False,
            buttons=buttons,
        )
        self.sendables.append(s)

    async def ask_transcription(self, callback_data):
        voice_id = int(callback_data)

        Voice = get_voice_class()
        voice = await Voice.select_one(id=voice_id)

        executor_data = self.challenge.row.executor_data
        executor_data["voice_id"] = voice_id
        executor_data["phrase_id"] = voice.row.phrase_id
        await self.challenge.update(executor_data=Json(executor_data))

        voice_binary = await retrieve_binary(voice.row.s3_key)

        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] Write transcription.",
            is_reply=False,
            buttons=[],
        )
        self.sendables.append(s)
        s = Sendable(
            type=SendableTypeCode.SND_VOC,
            value=voice_binary,
            is_reply=False,
            buttons=[],
        )
        self.sendables.append(s)

    async def ask_submission(self, text, message_id):
        submit_button = Button(text="[TTT] Submit", data=message_id)
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="[TTT] Press 'Submit' to submit, or send another variant if you think you've made an error.",
            is_reply=True,
            buttons=[submit_button],
        )
        self.sendables.append(s)

    async def save_transcription(self, text, callback_data):
        executor_data = self.challenge.row.executor_data
        voice_id = executor_data["voice_id"]
        phrase_id = executor_data["phrase_id"]

        Phrase = get_phrase_class()
        phrase = await Phrase.select_one(id=phrase_id)
        Voice = get_voice_class()
        voice = await Voice.select_one(id=voice_id)

        length = voice.row.length
        lines = [
            f"[TTT] The original phrase was {phrase.row.original_text!r}",
            f"[TTT] Effective length = {length}",
        ]

        distance = get_distance(text, phrase.row.normalized_text)
        if distance > 0:
            xp = length - distance
            lines.append("[TTT] You transcribed it differently")
            lines.append(f"[TTT] Distance (penalty) = {distance}")
            lines.append(f"[TTT] Score = {length} - {distance} = {xp}")
        else:
            xp = length
            lines.append("[TTT] And you transcribed it right!")
            lines.append(f"[TTT] Score = {xp}")

        Transcription = get_transcription_class()
        await Transcription.add_from_challenge(voice_id, text, distance, self.challenge)

        Person = get_person_class()
        total_xp = await Person.increase_xp(
            xp,
            person_trs_id=self.challenge.row.person_id,
            person_voc_id=voice.row.person_id,
            person_phr_id=phrase.row.person_id,
        )
        lines.append(f"[TTT] Total score now = {total_xp}")

        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value="\n".join(lines),
            is_reply=False,
            buttons=[get_start_button()],
        )
        self.sendables.append(s)

        await self.challenge.update(
            is_active=False,
        )
