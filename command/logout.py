# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


@commands.command()
@commands.is_owner()
async def logout(ctx):
    await ctx.bot.logout()


def setup(bot):
    bot.add_command(logout)
