# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import json

import discord
from discord.ext import commands


class Settings:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed()
            embed.title = "Server Settings"
            embed.colour = 0x0099FF

            try:
                prefix = self.bot.prefixes[str(ctx.guild.id)]["prefix"]
            except:
                raise commands.NoPrivateMessage
            cmds = []

            for cmd in self.settings.commands:
                cmds.append(prefix + cmd.qualified_name)

            cmds = "` `".join(cmds)
            embed.description = f"**`{cmds}`**"
            await ctx.send(embed=embed)

    @settings.command()
    @commands.guild_only()
    async def prefix(self, ctx, prefix: str = None):
        if prefix is None:
            await ctx.send("Please specify a new prefix.")
            return

        del self.bot.prefixes[str(ctx.guild.id)]["prefix"]
        self.bot.prefixes[str(ctx.guild.id)]["prefix"] = prefix

        prefix = self.bot.prefixes[str(ctx.guild.id)]["prefix"]
        with open("prefixes.json", "w") as f:
            json.dump(self.bot.prefixes, f, indent=4)

        await ctx.send(f":white_check_mark: Server prefix set to `{prefix}`")


def setup(bot):
    bot.add_cog(Settings(bot))
