# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import os

import discord
from discord.ext import commands


class Help:
    """
    Command module for help-related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed()
        embed.title = f"{self.bot.user.name}"
        embed.colour = 0x0099FF
        embed.set_footer(text="Module names are case sensitive.")

        embed.description = (
            "`v!cmds [module]` returns a list of commands in the "
            "specified module.\n`v!modules` returns a list of available "
            "modules.\n~~`v!help [command]` returns information about the "
            "specified command.~~"
        )

        await ctx.author.send(embed=embed)
        await ctx.send(":mailbox_with_mail: Check your DMs")

    @commands.command()
    async def modules(self, ctx):
        embed = discord.Embed()
        embed.title = "Available Command Modules"
        embed.colour = 0x0099FF
        embed.set_footer(text="Module names are case sensitive.")
        mods = []

        for mod in self.bot.cogs:
            if str(mod) == "Owner":
                continue
            else:
                mods.append(mod)

        mods = "\n".join(mods)
        embed.description = mods
        await ctx.send(embed=embed)

    @commands.command()
    async def cmds(self, ctx, module: str = None):
        if module is None:
            await ctx.invoke(self.modules)
            return

        if str(module) == "Owner":
            await ctx.invoke(self.modules)
            return

        mod = self.bot.get_cog(module)
        if mod is None:
            await ctx.invoke(self.modules)
            return

        embed = discord.Embed()
        embed.title = f"{module} Commands"
        embed.colour = 0x0099FF
        cmds = []

        for cmd in self.bot.get_cog_commands(module):
            cmds.append("v!" + str(cmd))

        cmds = "` `".join(cmds)
        embed.description = f"`{cmds}`"
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
