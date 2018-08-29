# Procbot Copyright (C) 2018 sirtezza451
# The full license can be found at master/LICENSE

import datetime
import json
import sys
import traceback

import discord
from discord import utils
from discord.ext import commands

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.send(':x: This command can\'t be used in private messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.CheckFailure):
            await ctx.send(':no_entry_sign: You require the `Manage Messages` permission to use this command.')

        elif isinstance(error, commands.BadArgument):
            await ctx.send(':x: Please specify a **whole number** of messages to delete.')

        elif isinstance(error, commands.CommandInvokeError):
            if str(ctx.command) == 'mute':
                await ctx.send(':x: I require the `Manage Channels` permission to create a channel and log this case.')
            elif str(ctx.command) == 'purge':
                await ctx.send(':x: I require the `Manage Messages` and/or the `Read Message History` permission to run this command.')

        else:
            print(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)            

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason: str = None):
        with open('mod_logs.json', 'r') as fp:
            mod_logs = json.load(fp)

        if member is None:
            await ctx.send(':grey_exclamation: Please mention a member to mute.')
        elif member.id == ctx.author.id:
            await ctx.send(':grey_exclamation: Why would you want to mute yourself?')
        elif member.id == self.bot.user.id:
            await ctx.send(':grey_exclamation: Why would you want to mute me? I can\'t mute myself anyway.')
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(':no_entry_sign: You can\'t mute someone with a role higher than or equal to your role.')
        else:
            role = utils.get(ctx.guild.roles, name='Muted')
            if role in member.roles:
                await ctx.send(f':x: **{member.name}** has already been muted.')
                return

            if reason is None:
                reason = 'No reason given.'

            await member.add_roles(role)
            embed = discord.Embed()
            embed.title = ':zipper_mouth: Member Muted'
            embed.colour = 0x0000ff
            embed.add_field(name='Member Name', value=member.name, inline=False)
            embed.add_field(name='Member ID', value=member.id, inline=False)
            embed.add_field(name='Muted By', value=ctx.author.name, inline=False)
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.set_footer(text=datetime.datetime.now())
            await ctx.send(embed=embed)

            mod_logs[str(ctx.guild.id)]['MUTE_COUNT'] += 1
            with open('mod_logs.json', 'w') as fp:
                json.dump(mod_logs, fp, indent=4)
            await self.bot.on_mute(author=ctx.author, member=member, reason=str(reason))

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(':grey_exclamation: Please mention a member to unmute.')
        elif member.id == ctx.author.id:
            await ctx.send(':grey_exclamation: You\'re able to run this command, so you were never muted in the first place.')
        elif member.id == self.bot.user.id:
            await ctx.send(':grey_exclamation: I can\'t mute myself, so I guess I can\'t unmute myself.')
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(':no_entry_sign: You can\'t unmute someone with a role higher than or equal to your role.')
        else:
            role = utils.get(ctx.guild.roles, name='Muted')
            if not role in member.roles:
                await ctx.send(f':x: **{member.name}** was never muted.')
            else:
                await member.remove_roles(role)
                embed = discord.Embed()
                embed.title = ':open_mouth: Member Unmuted'
                embed.colour = 0x0000ff
                embed.add_field(name='Member Name', value=member.name, inline=False)
                embed.add_field(name='Member ID', value=member.id, inline=False)
                embed.add_field(name='Unmuted By', value=ctx.author.name, inline=False)
                embed.set_footer(text=datetime.datetime.now())
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int = None):
        if number is None:
            await ctx.send(':grey_exclamation: Please specify a number of messages to delete.')
        elif not 1 < number < 101:
            await ctx.send(':grey_exclamation: Please specify a number between `2` and `100`.')
        else:
            purged = await ctx.channel.purge(limit=number, check=None)
            embed = discord.Embed()
            embed.title = ':white_check_mark: Success!'
            embed.description = f'Successfully deleted **{len(purged)}** messages.'
            embed.colour = 0x00ff00
            embed.set_footer(text=datetime.datetime.now())
            await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))