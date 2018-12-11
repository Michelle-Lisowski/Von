# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import time


@commands.command()
async def ping(ctx):
    embed = discord.Embed()
    embed.colour = 0x0099FF
    embed.title = ctx.bot.user.name

    embed.description = f":ping_pong: Pong!"
    embed.set_footer(text=f"Websocket Latency: {round(ctx.bot.latency * 1000)}ms")
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(ping)
