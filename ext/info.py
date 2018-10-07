"""
The MIT License (MIT)

Copyright (c) 2018 sirtezza451

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import sys
import time
import traceback

import discord
from discord.ext import commands

start_time = time.time()

class Information:
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.send(':x: This command can\'t be used in private messages.')
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            await ctx.send(':x: I could not find that member.')

        else:
            print(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command()
    async def info(self, ctx):
        seconds = time.time() - start_time
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        embed = discord.Embed()
        embed.title = 'Jaffa'
        embed.description = '**Jaffa by sirtezza_451#9856. Created using discord.py rewrite.**'
        embed.colour = 0x0099ff
        embed.add_field(name='Uptime', value=f'Jaffa has been awake for **{round(days)} days, {round(hours)} hours, {round(minutes)} minutes, and {round(seconds)} seconds.**', inline=False)
        embed.add_field(name='Username', value=str(self.bot.user), inline=True)
        embed.add_field(name='ID', value=self.bot.user.id, inline=True)
        embed.add_field(name='Version', value='v1.3.2', inline=True)
        embed.add_field(name='Server Count', value=len(self.bot.guilds), inline=True)
        embed.add_field(name='User Count', value=len(self.bot.users), inline=True)
        embed.add_field(name='Python Version', value='v{0.major}.{0.minor}.{0.micro}'.format(sys.version_info), inline=True)
        embed.add_field(name='Discord Bots Page', value='https://discordbots.org/bot/477014316063784961', inline=False)
        embed.add_field(name='Source Code', value='https://github.com/sirtezza451/Jaffa', inline=False)
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
        embed.title = 'Jaffa'
        embed.colour = 0x0099ff
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Username', value=str(member), inline=True)
        embed.add_field(name='User ID', value=str(member.id), inline=True)
        embed.add_field(name='Role', value=str(member.top_role), inline=True)
        embed.add_field(name='Status', value=str(self.bot.get_status(member)), inline=True)
        embed.add_field(name='Activity', value=f'{str(self.bot.get_at(member))} **{str(activity)}**', inline=True)
        embed.add_field(name='Nickname', value=str(member.nick), inline=True)
        embed.add_field(name='Created', value=str(member.created_at), inline=False)
        embed.add_field(name='Joined', value=str(member.joined_at), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed()
        embed.title = 'Jaffa'
        embed.colour = 0x0099ff
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
