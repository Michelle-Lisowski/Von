# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


@commands.command()
async def skip(ctx):
    ctx.voice_client.stop()


def setup(bot):
    bot.add_command(skip)
