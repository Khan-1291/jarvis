import asyncio
import threading

from ui.main_window import VoiceImagePlayer, edge_speak
from voice.speech_to_text import  record_voice
from llm.groq_client import get_response
from skills.aircraft_skill import handle_aircraft_command


async def get_voice_input():
    """
    Run blocking microphone recording in a thread
    so asyncio loop does not freeze.
    """
    return await asyncio.to_thread(record_voice)


async def ai_loop(player):
    """
    Main AI processing loop
    """
    while True:
        try:
            user_text = await get_voice_input()

            if not user_text:
                continue

            player.write_log(f"You: {user_text}")

            # Skill handling first
            handled = handle_aircraft_command(user_text, player)
            if handled:
                continue

            # LLM response
            response = get_response(user_text)
            print("AI:", response)

            player.write_log(f"AI: {response}")
            edge_speak(response, player)

        except Exception as e:
            print("Error in AI loop:", e)


def start_async_loop(player):
    """
    Run asyncio loop in separate thread
    """
    asyncio.run(ai_loop(player))


def main():
    player = VoiceImagePlayer("assets/face.png", size=(900, 900))

    # Start AI loop in background thread
    threading.Thread(
        target=start_async_loop,
        args=(player,),
        daemon=True
    ).start()

    # Start UI loop
    player.root.mainloop()


if __name__ == "__main__":
    main()
