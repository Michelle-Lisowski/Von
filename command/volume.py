# -*- coding: utf-8 -*-

import asyncio

from discord.ext import commands

from utils import get_player


@commands.command()
async def volume(ctx, volume: int = None):
    player = get_player(ctx)

    if volume is None:
        current = round(player.entry.volume * 100)
        return await ctx.send(f":sound: Current volume level: **{current}%**.")
    elif not 0 < volume < 101:
        return await ctx.send(
            ":grey_exclamation: Please specify a volume level between `1` and `100`."
        )

    async with ctx.typing():
        if volume / 100 > player.entry.volume:
            while volume / 100 > player.entry.volume:
                player.entry.volume += 0.0001
                await asyncio.sleep(0.00001)
        elif volume / 100 < player.entry.volume:
            while volume / 100 < player.entry.volume:
                player.entry.volume -= 0.0001
                await asyncio.sleep(0.00001)
        else:
            player.entry.volume = volume / 100

    new = round(player.entry.volume * 100)
    await ctx.send(f":sound: Volume level set to **{new}%**.")


def setup(bot):
    bot.add_command(volume)
