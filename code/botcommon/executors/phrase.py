import string

from botcommon.bottypes import PhraseStates, Sendable, Button, SendableTypeCode, Stickers
from botcommon.config import config
from botcommon.helpers import get_start_button

from .baseexecutor import BaseExecutor


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
        tr = string.Template(_(
            "Please, help me collect more phrases in my database."
            "\nSend me a new <b>phrase</b> in $language."
            "\nSpell numbers as words: <i>two</i>, <i>three</i>..., not <i>2</i>, <i>3</i>..."
            "\nYou can send many variants but only submit one."
            "\n(Send /$cmd_start if you want to skip.)"
        ))
        tr = tr.substitute(
            language=config.CMPDBOT_LANGUAGE_HUMANS,
            cmd_start=_("start  // command"),
        )
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value=tr,
            is_reply=False,
            buttons=[],
        )
        self.sendables.append(s)

        s = Sendable(
            type=SendableTypeCode.SND_STK,
            value=Stickers.PHR,
            is_reply=False,
            buttons=[],
        )
        self.sendables.append(s)

    async def ask_submission(self, text, message_id):
        variant_num = await self.next_variant_num()
        submit_button = Button(text=_("Submit  // button"), data=message_id)
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value=str(variant_num),
            is_reply=True,
            buttons=[submit_button],
        )
        self.sendables.append(s)

    async def save_phrase(self, text, message_id):
        Phrase = get_phrase_class()
        await Phrase.add_from_challenge(text, self.challenge)

        tr = _(
            "Successfully saved. Thank you for help!"
            "\nYou can do the next challenge now."
        )
        s = Sendable(
            type=SendableTypeCode.SND_TXT,
            value=tr,
            is_reply=False,
            buttons=[],
        )
        self.sendables.append(s)

        s = Sendable(
            type=SendableTypeCode.SND_STK,
            value=Stickers.OK_PHR,
            is_reply=False,
            buttons=[get_start_button()],
        )
        self.sendables.append(s)

        await self.challenge.update(
            is_active=False,
        )
