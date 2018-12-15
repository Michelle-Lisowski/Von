# -*- coding: utf-8 -*-

import random

from discord.ext import commands


@commands.command()
async def roll(ctx, minimum: int = None, maximum: int = None):
    if maximum is None and minimum is not None:
        maximum = minimum
        minimum = 1
    elif minimum is None and maximum is None:
        minimum = 1
        maximum = 6

    if minimum > maximum:
        minimum, maximum = maximum, minimum

    result = random.randint(minimum, maximum)
    message = await ctx.send(":game_die: The die rolls...")

    cache = await ctx.get_message(message.id)
    await cache.edit(content=f":game_die: The die rolls: **{result}**")


def setup(bot):
    bot.add_command(roll)
