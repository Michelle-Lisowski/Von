# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

class Administration:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(":grey_exclamation: Please specify a member.")
        elif member.id == ctx.author.id:
            await ctx.send(
                ":grey_exclamation: Why would you want to ban yourself?"
            )
        elif member.id == self.bot.user.id:
            await ctx.send(":grey_exclamation: Why would you want to ban me?")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(
                ":no_entry_sign: Maybe try banning someone with a role lower "
                "than yours."
            )
        else:
            logs = discord.utils.get(ctx.guild.text_channels, name="logs")
            await ctx.guild.ban(member)
            await ctx.send(
                f":white_check_mark: Successfully banned `{str(member)}`.\n"
                f"Ban details are in <#{logs.id}>."
            )


def setup(bot):
    bot.add_cog(Administration(bot))
