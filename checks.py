# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


def is_enabled(ctx):
    try:
        disabled_commands = ctx.bot.custom[str(ctx.guild.id)]["DISABLED_COMMANDS"]
    # An AttributeError would happen in DMs, since the guild attribute doesn't exist
    except (KeyError, AttributeError):
        disabled_commands = []

    if str(ctx.command) in disabled_commands:
        raise commands.DisabledCommand(
            f":exclamation: Command `{ctx.command}` has been disabled."
        )
    return True


def setup(bot):
    bot.add_check(is_enabled)
