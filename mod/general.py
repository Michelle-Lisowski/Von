# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


class General:
    """
    Command module for general commands.

    These include `v!ping` and `v!avatar`.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed()
        embed.title = self.bot.user.name
        embed.description = ":ping_pong: Pong!"
        embed.colour = 0x0099FF
        embed.set_footer(text=f"This took {latency} ms.")
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed()
        embed.title = member.name
        embed.colour = 0x0099FF
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
