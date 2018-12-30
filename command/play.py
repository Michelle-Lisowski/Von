# -*- coding: utf-8 -*-

from discord.ext import commands

from utils import Source, get_player


@commands.command()
async def play(ctx, *, search_term: str):
    player = get_player(ctx)

    async with ctx.typing():
        source = await Source.download(ctx, search_term)
        player.put(source)


def setup(bot):
    bot.add_command(play)
