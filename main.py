import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import AssistantFnc

load_dotenv()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=("You will act as an AI voice assistant that responds and interfaces with usesr onyl by voice,"
              "Give short and concise responses to user queries."),
    )

    # Subscribe to audio track, no video
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFnc()

    assistant = VoiceAssistant(
        # Voice activity detection
        vad=silero.VAD.load(),
        # Speech to text
        stt=openai.STT(),
        # Language model
        llm=openai.LLM(),
        # Text to speech
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )
    # Start audio only room from Livekit
    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("Hello, I am a voice assistant. How can I help you today?", allow_interruptions=True)


if __name__ == "__main__":
    # Starts chat agent
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
