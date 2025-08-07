# imports

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    elevenlabs,
    deepgram,
    noise_cancellation,
)
from livekit.plugins import silero  
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION

load_dotenv()
import os
print("DEBUG: ELEVEN_API_KEY loaded:", "Yes" if os.getenv("ELEVEN_API_KEY") else "No")
print("DEBUG: OPENAI_API_KEY loaded:", "Yes" if os.getenv("OPENAI_API_KEY") else "No")

# Test ElevenLabs API key and credits
async def test_elevenlabs_key():
    import aiohttp
    api_key = "sk_b62d5bcb573fbc0e0275c7f6abb393dcbdfbb687e119acfb"  
    
    async with aiohttp.ClientSession() as session:
        headers = {"xi-api-key": api_key}
        
        
        async with session.get("https://api.elevenlabs.io/v1/user", headers=headers) as response:
            print(f"API Key Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                print(f"Credits remaining: {data.get('subscription', {}).get('character_count', 'Unknown')}")
                print(f"Character limit: {data.get('subscription', {}).get('character_limit', 'Unknown')}")
            else:
                print(f"Error: {await response.text()}")
        
        
        async with session.get("https://api.elevenlabs.io/v1/voices", headers=headers) as voices_response:
            if voices_response.status == 200:
                voices_data = await voices_response.json()
                print("\nAvailable voices in your account:")
                for voice in voices_data.get('voices', []):
                    print(f"  Name: {voice['name']} - ID: {voice['voice_id']} - Category: {voice.get('category', 'unknown')}")
            else:
                print(f"Voices error: {await voices_response.text()}")


# Uncomment the next 3 lines to test API key first
# import asyncio
# asyncio.run(test_elevenlabs_key())
# exit()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTION)


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=openai.LLM(
            model="gpt-4o-mini",  # or "gpt-4o" for higher quality but more expensive
            temperature=0.8,
        ),
        tts=elevenlabs.TTS(
            voice_id="tObVwVIF5SYVbriX3vPM",  # My custon voice id
            model="eleven_turbo_v2_5",  # Fast model for real-time
            api_key="sk_b62d5bcb573fbc0e0275c7f6abb393dcbdfbb687e119acfb",  
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))