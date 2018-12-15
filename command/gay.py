# -*- coding: utf-8 -*-

import random

import discord
from discord.ext import commands


@commands.command()
async def gay(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    percentage = random.randint(1, 100)
    emoji = ":smiley:" if percentage < 50 else ":gay_pride_flag:"

    embed = discord.Embed()
    embed.colour = 0x0099FF
    embed.title = ctx.bot.user.name

    embed.description = f"{emoji} **{member.name}** is {percentage}% gay."
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(gay)
