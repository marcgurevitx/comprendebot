
async def arrange_new_challenge(person, chat):
    challenge = await person.get_new_challenge()
    if challenge is None:
        await chat.send_text("[TTT] No challenge found. Please try later.")
    else:
        async with challenge.get_executor() as executor:
            await executor.start()
            sendables = executor.pop_sendables()
            await chat.send_list(sendables)
