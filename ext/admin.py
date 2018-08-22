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

import datetime
import json

import discord
from discord.ext import commands

class Administration:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason: str = None):
        with open('mod_logs.json', 'r') as fp:
            mod_logs = json.load(fp)

        if member is None:
            await ctx.send(':no_entry_sign: You didn\'t mention a member to be kicked!')
            return
        elif member.id == ctx.author.id:
            await ctx.send(':no_entry_sign: Surely you don\'t want to kick yourself!')
            return
        elif member.id == self.bot.user.id:
            await ctx.send(':no_entry_sign: I can\'t kick myself! Why would you want to kick me anyway?')
            return
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(':no_entry_sign: You can\'t kick someone with a role equal to or higher than your role!')
            return
        else:
            if reason is None:
                reason = 'No reason given.'

            await ctx.guild.kick(user=member)
            embed = discord.Embed()
            embed.title = ':boot: Member Kicked'
            embed.colour = 0x0000ff
            embed.add_field(name='Member Name', value=member.name, inline=False)
            embed.add_field(name='Member ID', value=member.id, inline=False)
            embed.add_field(name='Kicked By', value=ctx.author.name, inline=False)
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.set_footer(text=datetime.datetime.now())
            await ctx.send(embed=embed)

            mod_logs[str(ctx.guild.id)]['KICK_CASES'] += 1
            with open('mod_logs.json', 'w') as fp:
                json.dump(mod_logs, fp, indent=4)
            await self.bot.on_kick(author=ctx.author, member=member, reason=str(reason))

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason: str = None):
        with open('mod_logs.json', 'r') as fp:
            mod_logs = json.load(fp)

        if member is None:
            await ctx.send(':no_entry_sign: You didn\'t mention a member to be banned!')
            return
        elif member.id == ctx.author.id:
            await ctx.send(':no_entry_sign: Surely you don\'t want to ban yourself!')
            return
        elif member.id == self.bot.user.id:
            await ctx.send(':no_entry_sign: I can\'t ban myself! Why would you want to ban me anyway?')
            return
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(':no_entry_sign: You can\'t ban someone with a role equal to or higher than your role!')
            return
        else:
            if reason is None:
                reason = 'No reason given.'

            await ctx.guild.ban(user=member)
            embed = discord.Embed()
            embed.title = ':no_entry_sign: Member Banned'
            embed.colour = 0x0000ff
            embed.add_field(name='Member Name', value=member.name, inline=False)
            embed.add_field(name='Member ID', value=member.id, inline=False)
            embed.add_field(name='Banned By', value=ctx.author.name, inline=False)
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.set_footer(text=datetime.datetime.now())
            await ctx.send(embed=embed)

            mod_logs[str(ctx.guild.id)]['BAN_CASES'] += 1
            with open('mod_logs.json', 'w') as fp:
                json.dump(mod_logs, fp, indent=4)
            await self.bot.on_ban(author=ctx.author, member=member, reason=None)

def setup(bot):
    bot.add_cog(Administration(bot))
