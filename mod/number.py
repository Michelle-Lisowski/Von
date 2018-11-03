# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import random

import discord
from discord.ext import commands

class Number:
    """
    Command module for number-based commands
    (other than `v!calculator`)

    List of commands:
    ```
    v!gay
    v!roll
    ```
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gay(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed()
        embed.title = self.bot.user.name
        embed.colour = 0x0099FF

        pct = random.randint(1, 100)

        if pct < 50:
            emoji = ":smiley:"
        else:
            emoji = ":gay_pride_flag:"

        embed.description = f"{emoji} **{member.name}** is {pct}% gay."
        embed.set_footer(text="Disclaimer: this calculation is 100% inaccurate.")
        await ctx.send(embed=embed)

    @commands.command()
    async def roll(self, ctx):
        result = random.randint(1, 6)
        msg = await ctx.send(":game_die: The die rolls...")

        cache = await ctx.get_message(msg.id)
        await cache.edit(content=f":game_die: The die rolls: **{result}**!")

def setup(bot):
    bot.add_cog(Number(bot))
