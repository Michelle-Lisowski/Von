# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import aiohttp


class Image:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        async with ctx.typing():
            embed = discord.Embed()
            embed.title = ":cat: Meow"
            embed.colour = 0x0099FF

            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    f = await r.json()
                    embed.set_image(url=f["file"])
            await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        async with ctx.typing():
            embed = discord.Embed()
            embed.title = ":dog: Woof"
            embed.colour = 0x0099FF

            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://dog.ceo/api/breeds/image/random") as r:
                    f = await r.json()
                    embed.set_image(url=f["message"])
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Image(bot))
