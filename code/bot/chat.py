from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from botcommon.bottypes import Sendable, SendableTypeCode, Stickers
from botcommon.config import config


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
        elif sendable.type == SendableTypeCode.SND_STK:
            if sendable.value == Stickers.PHR:
                sticker = config.STICKER_PHR
            elif sendable.value == Stickers.VOC:
                sticker = config.STICKER_VOC
            elif sendable.value == Stickers.TRS:
                sticker = config.STICKER_TRS
            elif sendable.value == Stickers.GOLD:
                sticker = config.STICKER_GOLD
            elif sendable.value == Stickers.SILVER:
                sticker = config.STICKER_SILVER
            elif sendable.value == Stickers.BRONZE:
                sticker = config.STICKER_BRONZE
            elif sendable.value == Stickers.PAPER:
                sticker = config.STICKER_PAPER
            elif sendable.value == Stickers.OK_PHR:
                sticker = config.STICKER_OK_PHR
            elif sendable.value == Stickers.OK_VOC:
                sticker = config.STICKER_OK_VOC
            else:
                raise Exception(f"Unknown sticker [{sendable}]")

            await self.bot.send_sticker(
                chat_id=self.chat_id,
                sticker=sticker,
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
