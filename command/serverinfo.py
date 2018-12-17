# -*- coding: utf-8 -*-

from datetime import datetime

import discord
from discord.ext import commands

import utils


@commands.command()
async def serverinfo(ctx):
    embed = discord.Embed()
    embed.colour = 0x0099FF
    embed.title = str(ctx.guild)

    verification = str(ctx.guild.verification_level).capitalize()
    created = str(ctx.guild.created_at).split(".")[0]
    region = utils.clean_region(str(ctx.guild.region))

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text="Some of this information may change.")

    embed.add_field(name="Server ID", value=ctx.guild.id)
    embed.add_field(name="Created At", value=created)

    embed.add_field(name="Member Count", value=len(ctx.guild.members))
    embed.add_field(name="Role Count", value=len(ctx.guild.roles))

    embed.add_field(name="Text Channel Count", value=len(ctx.guild.text_channels))
    embed.add_field(name="Voice Channel Count", value=len(ctx.guild.voice_channels))

    embed.add_field(name="Verification Level", value=verification)
    embed.add_field(name="Voice Region", value=region)
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(serverinfo)
