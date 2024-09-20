import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import AssistantFnc

load_dotenv()


async def entrypoint(ctx: JobContext):
    intial_ctx = llm.ChatContext().append(
        role="system",
        text=("Hello, I am a voice assistant. How can I help you today?"),
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
