import os
import glob
import discord
import PySimpleGUI as sg
import asyncio
import threading
from discord.ext import commands
from OutsideCommunicationCogModule import OutsideCommunicationCog
from SoundPlayingCogModule import SoundPlayingCog
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()
bot = commands.Bot(command_prefix='2!', description="This is 2B!")


TOKEN = os.getenv('TOKEN')

glob_ctx = None
glob_voice_channel = None

# Get sounds

sound_list = glob.glob("sound/*")

# Window
sg.theme('Black')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('2Bot command window')],
          [sg.Text('Text to say:'), sg.InputText()],
          [sg.Button('Say')],
          [sg.Listbox(values=sound_list, size=(30, 10), key="sounds")],
          [sg.Button('Play')]]

# Create the Window
window = sg.Window('Window Title', layout)

def update_ctx(ctx):
    global glob_ctx
    glob_ctx = ctx

def update_voice(voice):
    global glob_voice_channel
    glob_voice_channel = voice
# Events
@bot.event
async def on_ready():
    print('2Bot, ready for duty')

# Commands

@bot.command()
async def ping(ctx):
    update_ctx(ctx)
    await ctx.send('pong')

@bot.command()
async def test(ctx):
    update_ctx(ctx)
    await ctx.send("Yes, what is it?")

@bot.command()
async def join(ctx):
    update_ctx(ctx)
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    update_voice(vc)
    await ctx.send("Right away")

@bot.command()
async def leave(ctx):
    update_ctx(ctx)
    await ctx.voice_client.disconnect()

if __name__ == '__main__':
    print("Hello")

    bot_run_thread = threading.Thread(target=bot.run, args=[TOKEN])
    bot_run_thread.daemon = True
    bot_run_thread.start()

    cogs = [OutsideCommunicationCog(bot), SoundPlayingCog(bot)]
    outside_communication_cog = cogs[0]
    sound_playing_cog = cogs[1]
    for cog in cogs:
        bot.add_cog(cog)

    loop = asyncio.get_event_loop()

    # Window shite
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window
            break
        if event == "Say":
            if glob_ctx is not None:
                asyncio.run_coroutine_threadsafe(outside_communication_cog.say(glob_ctx, message=values[0]), loop)
        if event == "Play":
            if glob_voice_channel is not None:
                asyncio.run_coroutine_threadsafe(sound_playing_cog.play(glob_voice_channel, sound_list[window['sounds'].get_indexes()[0]]), loop)

    window.close()








