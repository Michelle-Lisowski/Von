# -*- coding: utf-8 -*-

import json

import discord
from discord.ext import commands


@commands.command()
@commands.has_permissions(manage_guild=True)
async def enable(ctx, *, command: str):
    cmds = [cmd.qualified_name for cmd in ctx.bot.commands]

    if not command in cmds:
        raise commands.CommandError(":exclamation: Command not found.")

    try:
        disabled_commands = ctx.bot.custom[str(ctx.guild.id)]["DISABLED_COMMANDS"]
    except KeyError:
        try:
            ctx.bot.custom[str(ctx.guild.id)]["DISABLED_COMMANDS"] = []
        except KeyError:
            ctx.bot.custom[str(ctx.guild.id)] = {}
            ctx.bot.custom[str(ctx.guild.id)]["DISABLED_COMMANDS"] = []
        disabled_commands = ctx.bot.custom[str(ctx.guild.id)]["DISABLED_COMMANDS"]

    if command in disabled_commands:
        disabled_commands.remove(command)
        await ctx.send(f":white_check_mark: Enabled command `{command}`.")
    else:
        await ctx.send(f":information_source: Command `{command}` was never disabled.")

    with open("custom.json", "w") as f:
        json.dump(ctx.bot.custom, f, indent=4)


def setup(bot):
    bot.add_command(enable)
