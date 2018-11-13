# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mute(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Please specify a member.")
        elif member.id == ctx.author.id:
            await ctx.send("Why would you want to mute yourself?")
        elif member.id == self.bot.user.id:
            await ctx.send("Why would you want to ban me?")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send("Maybe try kicking someone with a lower role than yours.")
        else:
            embed = discord.Embed()
            embed.title = "Mute"
            embed.colour = 0x0099FF

            await self.bot.mute(member)
            embed.add_field(name="Member", value=str(member))
            embed.add_field(name="Member ID", value=member.id)
            embed.add_field(name="Muted By", value=str(ctx.author))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
