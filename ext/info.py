"""
Procbot - A Discord bot which plays music, executes fun and admin commands, and more!
Copyright (C) 2018 sirtezza451

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.

The full license can be found at master/LICENSE.
"""

import sys
import time

import discord
from discord.ext import commands

start_time = time.time()

class Information:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        seconds = time.time() - start_time
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        embed = discord.Embed()
        embed.title = 'Procbot'
        embed.description = '**Procbot by sirtezza_451#9856. Created using discord.py rewrite.**'
        embed.colour = 0x0000ff
        embed.add_field(name='Uptime', value=f'Procbot has been awake for **{round(days)} days, {round(hours)} hours, {round(minutes)} minutes, and {round(seconds)} seconds.**', inline=False)
        embed.add_field(name='Name', value=f'{self.bot.user.name}#{self.bot.user.discriminator}', inline=True)
        embed.add_field(name='ID', value=self.bot.user.id, inline=True)
        embed.add_field(name='Version', value='v1.0.0', inline=True)
        embed.add_field(name='Server Count', value=len(self.bot.guilds), inline=True)
        embed.add_field(name='User Count', value=len(self.bot.users), inline=True)
        embed.add_field(name='Python Version', value='v{0.major}.{0.minor}.{0.micro}'.format(sys.version_info), inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def profile(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        if member.activity is None:
            activity = '\uFEFF'
        else:
            activity = member.activity

        embed = discord.Embed()
        embed.title = 'Procbot'
        embed.colour = 0x0000ff
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Username', value=str(member), inline=True)
        embed.add_field(name='User ID', value=str(member.id), inline=True)
        embed.add_field(name='Role', value=str(member.top_role), inline=True)
        embed.add_field(name='Status', value=str(self.bot.get_status(member)), inline=True)
        embed.add_field(name='Activity', value=f'{str(self.bot.get_at(member))} {str(activity)}', inline=True)
        embed.add_field(name='Nickname', value=str(member.nick), inline=True)
        embed.add_field(name='Created', value=str(member.created_at), inline=False)
        embed.add_field(name='Joined', value=str(member.joined_at), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed()
        embed.title = 'Procbot'
        embed.colour = 0x0000ff
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name='Server Name', value=str(guild.name), inline=True)
        embed.add_field(name='Server ID', value=str(guild.id), inline=True)
        embed.add_field(name='Owner Name', value=str(guild.owner), inline=True)
        embed.add_field(name='Owner ID', value=str(guild.owner.id), inline=True)
        embed.add_field(name='Verification Level', value=str(self.bot.get_vl(ctx.guild)), inline=True)
        embed.add_field(name='Voice Region', value=str(self.bot.get_vr(ctx.guild)), inline=True)
        embed.add_field(name='Role Count', value=str(len(guild.roles)), inline=True)
        embed.add_field(name='Channel Count', value=str(len(guild.text_channels) + len(guild.voice_channels)), inline=True)
        embed.add_field(name='Member Count', value=str(len(guild.members)), inline=False)
        embed.add_field(name='Created', value=str(guild.created_at), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Information(bot))
