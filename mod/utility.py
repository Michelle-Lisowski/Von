# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import aiohttp
import discord
from discord.ext import commands


class Utility:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def urban(self, ctx, *, search: str = None):
        if search is None:
            await ctx.send("Please specify a search term.")
            return

        async with ctx.typing():
            embed = discord.Embed()
            embed.colour = 0x0099FF

            ud = "http://api.urbandictionary.com/v0"

            async with self.bot.session.get(f"{ud}/define?term={search}") as r:
                f = await r.json()

                try:
                    a = f["list"][0]
                except:
                    await ctx.send(":mag: No results found.")
                    return

            d = a["definition"].replace("[", "").replace("]", "")
            embed.title = a["word"]
            embed.description = d
            embed.set_footer(text=f"Author: {a['author']}")
            await ctx.send(embed=embed)

    @commands.command(aliases=["calc"])
    async def calculator(self, ctx, *, expression: str = None):
        if expression is None:
            await ctx.send("Please specify an expression.")
            return

        async with ctx.typing():
            e = expression.lower().replace("x", "*").replace("^", "**")

            try:
                result = eval(e, None, locals())
            except:
                await ctx.send(f"`{expression}` contains invalid arguments.")
            else:
                await ctx.send(
                    f"According to my calculations, the answer is **{result}**."
                )

    @commands.command()
    async def weather(self, ctx, *, location: str = None):
        if location is None:
            await ctx.send("Please specify a location.")
            return

        async with ctx.typing():
            embed = discord.Embed()
            embed.colour = 0x0099FF

            mw = "https://metaweather.com/api"

            async with self.bot.session.get(
                f"{mw}/location/search/?query={location}", ssl=False
            ) as s:
                l = await s.json()

            try:
                async with self.bot.session.get(
                    f"{mw}/location/{l[0]['woeid']}", ssl=False
                ) as r:
                    f = await r.json()
                    w = f["consolidated_weather"][0]
            except IndexError:
                await ctx.send(f":mag: No results found for `{location}`.")
                return

            embed.title = l[0]["title"]
            embed.add_field(name="Weather State", value=w["weather_state_name"])
            embed.add_field(
                name="Current Temperature", value=f"{round(w['the_temp'])}°C"
            )
            embed.add_field(
                name="Minimum Temperature", value=f"{round(w['min_temp'])}°C"
            )
            embed.add_field(
                name="Maximum Temperature", value=f"{round(w['max_temp'])}°C"
            )
            embed.add_field(name="Wind Direction", value=w["wind_direction_compass"])
            embed.add_field(name="Wind Speed", value=f"{round(w['wind_speed'])} mph")
            embed.add_field(name="Humidity", value=f"{round(w['humidity'])}%")
            embed.set_footer(text="Source: https://metaweather.com")
            await ctx.send(embed=embed)

    @commands.command()
    async def eval(self, ctx, *, code: str = None):
        if code is None:
            await ctx.send("Please specify code to evaluate.")
            return

        try:
            e = eval(code, None, locals())
        except:
            await ctx.send(f"The code contains invalid syntax.")
        else:
            await ctx.send(f"```python\n{e}\n```")


def setup(bot):
    bot.add_cog(Utility(bot))
