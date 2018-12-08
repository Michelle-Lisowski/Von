# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


@commands.command()
@commands.is_owner()
async def unload(ctx, extension: str):
    try:
        ctx.bot.unload_extension(extension)
    except (discord.ClientException, ModuleNotFoundError):
        raise commands.CommandError(":exclamation: An error occurred.")
    else:
        await ctx.send(f":white_check_mark: Unloaded extension `{extension}`.")


def setup(bot):
    bot.add_command(unload)
