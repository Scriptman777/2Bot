from typing import Optional

import discord
from discord.ext.commands import command, Context, Bot, Cog
from discord import VoiceClient


class SoundPlayingCog(Cog):
    bot: Bot

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def play(self, voice_client: VoiceClient, path: str):
        if voice_client is None:
            print("No information to play")
        else:
            await voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/uzivatel/Documents/FFMPEG/bin/ffmpeg.exe", source=path))

