# -*- coding: utf-8 -*-

from discord.ext import commands

from utils import get_player


@commands.command()
async def stop(ctx):
    player = get_player(ctx)
    player.cleanup()

    await ctx.send(":information_source: Music stopped.")


def setup(bot):
    bot.add_command(stop)
