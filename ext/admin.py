# Procbot Copyright (C) 2018 sirtezza451
# The full license can be found at master/LICENSE

import datetime
import json
import sys
import traceback

import discord
from discord import utils
from discord.ext import commands

class MissingStaffRole(commands.CommandError):
    pass

class RoleHierarchyError(commands.CommandError):
    pass

class Administration:
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.send(':x: This command can\'t be used in private messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, MissingStaffRole):
            await ctx.send(':no_entry_sign: You require the `Staff` role to use this command.')

        elif isinstance(error, RoleHierarchyError):
            await ctx.send(error)

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(':x: I require the `Manage Channels` permission to create a channel and log this case.')

        else:
            print(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command()
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member = None, *, reason: str = None):
        staff_role = utils.get(ctx.guild.roles, name='Staff')
        with open('mod_logs.json', 'r') as fp:
            mod_logs = json.load(fp)

        if member is None:
            await ctx.send(':grey_exclamation: Please mention a member to kick.')
        elif member.id == ctx.author.id:
            await ctx.send(':grey_exclamation: Why would you want to kick yourself?')
        elif member.id == self.bot.user.id:
            await ctx.send(':grey_exclamation: Why would you want to kick me? I can\'t kick myself anyway.')
        elif staff_role in member.roles:
            await ctx.send(':no_entry_sign: You can\'t kick someone who also has the `Staff` role.')
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(':no_entry_sign: You can\'t kick someone with a role higher than or equal to your role.')
        elif member.top_role >= ctx.guild.me.top_role:
            raise RoleHierarchyError(':x: The mentioned member has a role higher than or equal to my role.')
        elif not staff_role in ctx.author.roles:
            raise MissingStaffRole
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

            mod_logs[str(ctx.guild.id)]['KICK_COUNT'] += 1
            with open('mod_logs.json', 'w') as fp:
                json.dump(mod_logs, fp, indent=4)
            await self.bot.on_kick(author=ctx.author, member=member, reason=str(reason))

    @commands.command()
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member = None, *, reason: str = None):
        staff_role = utils.get(ctx.guild.roles, name='Staff')
        with open('mod_logs.json', 'r') as fp:
            mod_logs = json.load(fp)

        if member is None:
            await ctx.send(':grey_exclamation: Please mention a member to ban.')
        elif member.id == ctx.author.id:
            await ctx.send(':grey_exclamation: Why would you want to ban yourself?')
        elif member.id == self.bot.user.id:
            await ctx.send(':grey_exclamation: Why would you want to ban me? I can\'t ban myself anyway.')
        elif staff_role in member.roles:
            await ctx.send(':no_entry_sign: You can\'t ban someone who also has the `Staff` role.')
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(':no_entry_sign: You can\'t ban someone with a role higher than or equal to your role.')
        elif member.top_role >= ctx.guild.me.top_role:
            raise RoleHierarchyError(':x: The mentioned member has a role higher than or equal to my role.')
        elif not staff_role in ctx.author.roles:
            raise MissingStaffRole
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

            mod_logs[str(ctx.guild.id)]['BAN_COUNT'] += 1
            with open('mod_logs.json', 'w') as fp:
                json.dump(mod_logs, fp, indent=4)
            await self.bot.on_ban(author=ctx.author, member=member, reason=None)

def setup(bot):
    bot.add_cog(Administration(bot))
