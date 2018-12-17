# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


@commands.command()
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    embed = discord.Embed()
    embed.colour = 0x0099FF
    embed.title = member.display_name

    created = str(member.created_at).split(".")[0]
    status = (
        str(member.status).capitalize()
        if str(member.status) != "dnd"
        else "Do Not Disturb"
    )

    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text="Some of this information may change.")

    embed.add_field(name="User Name", value=member)
    embed.add_field(name="User ID", value=member.id)

    embed.add_field(name="Role Count", value=len(member.roles))
    embed.add_field(name="Top Role", value=member.top_role)

    embed.add_field(name="Created At", value=created)
    embed.add_field(name="Status", value=status)
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(profile)
