# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


@commands.command()
async def info(ctx):
    embed = discord.Embed()
    embed.colour = 0x0099FF
    embed.title = ctx.bot.user.name
    info = ctx.bot.process.as_dict(attrs=["cpu_percent", "num_threads", "memory_info"])

    embed.add_field(
        name="Memory Usage", value=f"{info['memory_info']._asdict()['vms'] >> 20} MB"
    )
    embed.add_field(name="CPU Usage", value=f"{round(info['cpu_percent'], 1)}%")
    embed.add_field(name="Thread Count", value=f"{info['num_threads']} Threads")
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(info)
