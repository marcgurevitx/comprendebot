class Chat:

    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    async def send_text(self, text):
        await self.bot.send_message(chat_id=self.chat_id, text=text)

    async def send(self, sendable):
        await self.bot.send_message(chat_id=self.chat_id, text=repr(sendable))
