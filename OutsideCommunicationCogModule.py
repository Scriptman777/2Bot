from typing import Optional

from discord import TextChannel
from discord.ext.commands import command, Context, Bot, Cog


class OutsideCommunicationCog(Cog):
    bot: Bot

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def say(self, ctx: Optional[Context], message: str, *, channel_id=None):
        channel: TextChannel = self.bot.get_channel(channel_id) if channel_id is not None else ctx.channel
        if ctx is None:
            if channel_id is None:
                print("No information to communicate")

        await channel.send(content=message)