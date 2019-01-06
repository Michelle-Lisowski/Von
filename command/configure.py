# -*- coding: utf-8 -*-

import json

import discord
from discord.ext import commands


@commands.group()
async def configure(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed()
        embed.colour = 0x0099FF

        subcommands = []
        prefix = await ctx.bot.get_prefix(ctx.message)

        for command in ctx.command.commands:
            subcommands.append(f"`{prefix}{command}`")

        embed.title = "Configuration Options"
        embed.description = "\n".join(subcommands)
        await ctx.send(embed=embed)


@configure.command()
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, prefix: str):
    try:
        del ctx.bot.custom[str(ctx.guild.id)]["PREFIX"]
    except KeyError:
        pass

    try:
        ctx.bot.custom[str(ctx.guild.id)]["PREFIX"] = prefix
    except KeyError:
        ctx.bot.custom[str(ctx.guild.id)] = {}
        ctx.bot.custom[str(ctx.guild.id)]["PREFIX"] = prefix

    with open("custom.json", "w") as f:
        json.dump(ctx.bot.custom, f, indent=4)

    prefix = ctx.bot.custom[str(ctx.guild.id)]["PREFIX"]
    await ctx.send(f":white_check_mark: Bot prefix set to `{prefix}`.")


def setup(bot):
    bot.add_command(configure)
