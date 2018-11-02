# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import aiohttp


class Utility:
    """
    Command module for utility commands

    List of commands:
    ```
    v!urban
    ```
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def urban(self, ctx, *, search: str = None):
        if search is None:
            await ctx.send(":grey_exclamation: Please specify a search term.")
            return

        async with ctx.typing():
            embed = discord.Embed()
            embed.colour = 0x0099FF

            ud = "http://api.urbandictionary.com/v0"

            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"{ud}/define?term={search}") as r:
                    f = await r.json()
                    a = f["list"][0]

            embed.title = a["word"]
            embed.description = a["definition"]
            embed.set_footer(text=f"Author: {a['author']}")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Urban(bot))
