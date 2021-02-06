from botcommon.bottypes import Sendable


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
        await self.bot.send_message(chat_id=self.chat_id, text=repr(sendable))
