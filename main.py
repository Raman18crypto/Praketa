'''
abbrevations:

variable name conventions:
ctx = Context,
vad = Voice Activity Detection,
stt = Speech to Text,
tts = Text to Speech,
chat_ctx = Chat Context,
fn_ctx = Function Context,

'''

import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import AssistantFnc

load_dotenv()

#creating the asynic function 

async def entrypoint(ctx: JobContext):
    #trigering code of the ai voice assistant function
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "Hello, I am a voice assistant created by Raman using the livekit platform."
            "Please specify the task you want me to perform."
        ),
        
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFnc() 
    # we can either connect to audio or video or both based on the requirement

    #defining the voice assistant to handle the audio track

    assistant = VoiceAssistant(
        vad = silero.VAD.load(),
        # to check if the user is speaking or not
        stt = openai.STT(),
        # openai is used to convert the speech to text
        llm = openai.LLM(),
        # to generate the response and we can use any model
        tts = openai.TTS(),
        # openai is used to convert the text to speech
        chat_ctx = initial_ctx,
        fnc_ctx = fnc_ctx,
    )

    assistant.start(ctx.room)
    # connecting to the room provided by the Jobcontext and start the assitant inside of the room.
    '''
    The agent is now connected to the Livekitserver and then the sever is gonna send the agent a job (task)
    then the agent will have a room assosiated with it.
    '''

    await asyncio.sleep(1)
    # waits for a second

    await assistant.say("Hey Boss, How can I help you today !!!", allow_interruptions=True)
    # the assistant will say the text provided in the argument and allow_intteruption is set to true as the user can interrupt the assistant at any time.


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint)) 
    #importing the cli from livekit
