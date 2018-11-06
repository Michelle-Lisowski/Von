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
            embed.title = "Setting Commands"
            embed.colour = 0x0099FF

            prefix = self.bot.prefixes[str(ctx.guild.id)]["prefix"]
            cmds = []

            for cmd in self.settings.commands:
                cmds.append(prefix + cmd.qualified_name)

            cmds = "` `".join(cmds)
            embed.description = f"**`{cmds}`**"
            await ctx.send(embed=embed)

    @settings.command()
    async def prefix(self, ctx, pfix: str = None):
        if pfix is None:
            await ctx.send("Please specify a new prefix.")
            return

        del self.bot.prefixes[str(ctx.guild.id)]["prefix"]
        self.bot.prefixes[str(ctx.guild.id)]["prefix"] = pfix

        prefix = self.bot.prefixes[str(ctx.guild.id)]["prefix"]
        with open("prefixes.json", "w") as f:
            json.dump(self.bot.prefixes, f, indent=4)

        await ctx.send(
            f":white_check_mark: Server prefix set to `{prefix}`"
        )

    
def setup(bot):
    bot.add_cog(Settings(bot))
