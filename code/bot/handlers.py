from aiogram import types


async def on_text(message: types.Message):
    await message.reply("Hello i bot!")
