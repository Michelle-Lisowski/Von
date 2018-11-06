# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Please specify a member.")
        elif member.id == ctx.author.id:
            await ctx.send(
                "Why would you want to kick yourself?"
            )
        elif member.id == self.bot.user.id:
            await ctx.send("Why would you want to kick me?")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(
                "Maybe try kicking someone with a role lower than yours."
            )
        else:
            await ctx.guild.kick(member)
            await ctx.send(
                f":white_check_mark: Successfully kicked **{member}**."
            )

    @commands.command()
    async def ban(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Please specify a member.")
        elif member.id == ctx.author.id:
            await ctx.send(
                "Why would you want to ban yourself?"
            )
        elif member.id == self.bot.user.id:
            await ctx.send("Why would you want to ban me?")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(
                "Maybe try banning someone with a role lower than yours."
            )
        else:
            logs = discord.utils.get(ctx.guild.text_channels, name="logs")
            await ctx.guild.ban(member)
            await ctx.send(
                f":white_check_mark: Successfully banned **{member}**.\n"
                f"Ban details are in <#{logs.id}>."
            )


def setup(bot):
    bot.add_cog(Admin(bot))
