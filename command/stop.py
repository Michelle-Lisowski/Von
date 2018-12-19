# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

from utils import get_player


@commands.command()
async def stop(ctx):
    player = get_player(ctx)
    player.loop.cancel()

    await player.ctx.voice_client.disconnect()
    del ctx.bot.players[str(ctx.guild.id)]
    await ctx.send(":information_source: Music stopped.")


def setup(bot):
    bot.add_command(stop)
