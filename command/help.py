# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


@commands.command()
async def help(ctx, command: str = None):
    prefix = await ctx.bot.get_prefix(ctx.message)

    if command is None or command == "help":
        embed = discord.Embed()
        embed.colour = 0x0099FF
        embed.title = "List of Commands"
        cmds = []

        for cmd in ctx.bot.commands:
            cmds.append(f"`{prefix}{cmd}`")

        embed.description = (
            f"Get more info by using `{prefix}help [command]`.\n" + "\n".join(cmds)
        )

        if ctx.guild is not None:
            await ctx.send(":mailbox_with_mail: Check your private messages.")

        await ctx.author.send(embed=embed)
        return

    cmd = ctx.bot.get_command(command)

    if cmd is None:
        raise commands.CommandError(f":exclamation: Command `{command}` not found.")

    embed = discord.Embed()
    embed.colour = 0x0099FF
    embed.title = f"`{prefix}{cmd}`"
    embed.description = "*insert placeholder here*"

    if ctx.guild is not None:
        await ctx.send(":mailbox_with_mail: Check your private messages.")
    await ctx.author.send(embed=embed)


def setup(bot):
    bot.add_command(help)
