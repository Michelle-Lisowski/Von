# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


def is_enabled(ctx):
    try:
        disabled_commands = ctx.bot.custom[str(ctx.guild.id)]["DISABLED_COMMANDS"]
    except KeyError:
        disabled_commands = []

    if str(ctx.command) in disabled_commands:
        raise commands.DisabledCommand(
            f":exclamation: Command `{ctx.command}` has been disabled."
        )
    return True


def setup(bot):
    bot.add_check(is_enabled)
