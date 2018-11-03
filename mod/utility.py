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
    v!calculator
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

    @commands.command(aliases=["calc"])
    async def calculator(self, ctx, *, expression: str):
        async with ctx.typing():
            e = expression.lower().replace("x", "*")

            try:
                result = eval(e, None, locals())
            except:
                await ctx.send(f":grey_exclamation: `{expression}` contains invalid arguments.")
            else:
                await ctx.send(f"According to my calculations, the answer is **{result}**.")

    @commands.command()
    async def weather(self, ctx, *, location: str):
        async with ctx.typing():
            embed = discord.Embed()
            embed.colour = 0x0099FF

            async with aiohttp.ClientSession() as cs:
                mw = "https://metaweather.com/api"
                async with cs.get(f"{mw}/location/search/?query={location}") as s:
                    l = await s.json()
                    async with cs.get(f"{mw}/location/{l['woeid']}") as r:
                        f = await r.json()

            embed.title = f["title"]
            embed.add_field(name="Weather State", value=f["weather_state_name"])
            embed.add_field(name="Current Temperature", value=f["the_temp"])
            embed.add_field(name="Minimum Temperature", value=f["min_temp"])
            embed.add_field(name="Maximum Temperature", value=f["max_temp"])
            embed.add_field(name="Humidity", value=f["humidity"])
            embed.add_field(name="Wind Direction", value=f["wind_direction"])
            embed.set_footer(text="Source: https://metaweather.com")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
