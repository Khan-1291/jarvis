import asyncio

async def input_loop(engine, record_voice):
    while True:
        voice_text = await asyncio.to_thread(record_voice)

        if voice_text:
            await engine.process(voice_text)
        else:
            user = await asyncio.to_thread(input, ">> ")
            if user:
                await engine.process(user)