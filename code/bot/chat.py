from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from botcommon.bottypes import Sendable, SendableTypeCode


class Chat:

    def __init__(self, bot, chat_id, recent_message):
        self.bot = bot
        self.chat_id = chat_id
        self.recent_message = recent_message

    async def send_list(self, sendables):
        for sendable in sendables:
            await self.send(sendable)

    async def send(self, sendable):
        assert isinstance(sendable, Sendable)
        send_params = self._prepare_params(sendable)

        if sendable.type == SendableTypeCode.SND_TXT:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=sendable.value,
                **send_params,
            )
        elif sendable.type == SendableTypeCode.SND_VOC:
            await self.bot.send_voice(
                chat_id=self.chat_id,
                voice=sendable.value,
                **send_params,
            )
        else:
            raise Exception(f"Sendable of unknown type [{sendable}]")

    def _prepare_params(self, sendable):
        rv = {}
        if sendable.is_reply:
            rv["reply_to_message_id"] = self.recent_message.message_id
        if sendable.buttons:
            keyboard = InlineKeyboardMarkup()
            for button_item in sendable.buttons:
                keyboard.add(InlineKeyboardButton(
                    button_item.text,
                    callback_data=button_item.data,
                ))
            rv["reply_markup"] = keyboard
        return rv

    async def send_simple_text(self, text):
        await self.send(Sendable(
            type=SendableTypeCode.SND_TXT,
            value=text,
            is_reply=False,
            buttons=[],
        ))
