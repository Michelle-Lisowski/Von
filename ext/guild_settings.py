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

import json
import random
import sys
import traceback

import discord
from discord import utils
from discord.ext import commands

from main import handler, logger

def is_guild_owner():
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner.id
    return commands.check(predicate)

class MissingPermissions(commands.CommandError):
    pass

class GuildSettings:
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.send(':x: This command can\'t be used in private messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.CheckFailure):
            await ctx.send(':no_entry_sign: You must be the owner of this server to use this command.')

        elif isinstance(error, commands.BadArgument):
            await ctx.send(':x: Please specify a **whole number** for the new default volume.')

        else:
            # print(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':', file=sys.stderr)
            # traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            logger.warning(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':')
            logger.error(traceback.format_exc())

    @commands.group(aliases=['settings'])
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            subcommands = '`prefix` `default_volume`'
            await ctx.send(f':grey_exclamation: Please specify one of the following subcommands:\n{subcommands}')

    @setting.command()
    @commands.guild_only()
    @is_guild_owner()
    async def prefix(self, ctx, new_prefix: str = None):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)

        if str(ctx.guild.id) in guilds:
            if new_prefix is None:
                await ctx.send(f":information_source: Current server prefix: **{guilds[str(ctx.guild.id)]['GUILD_PREFIX']}**")
            else:
                del guilds[str(ctx.guild.id)]['GUILD_PREFIX']
                guilds[str(ctx.guild.id)]['GUILD_PREFIX'] = new_prefix
                await ctx.send(f":information_source: New server prefix: **{new_prefix}**")
        else:
            if new_prefix is None:
                await ctx.send(':information_source: Current server prefix: **.**')
            else:
                guilds[str(ctx.guild.id)] = {}
                guilds[str(ctx.guild.id)]['GUILD_PREFIX'] = new_prefix
                await ctx.send(f":information_source: New server prefix: **{new_prefix}**")

        with open('guilds.json', 'w') as fp:
            json.dump(guilds, fp, indent=4)

    @setting.command()
    @commands.guild_only()
    @is_guild_owner()
    async def default_volume(self, ctx, new_volume: int = None):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)

        if str(ctx.guild.id) in guilds:
            if new_volume is None:
                await ctx.send(f":information_source: Current default volume: **{round(guilds[str(ctx.guild.id)]['DEFAULT_VOLUME'] * 100)}%**")
            else:
                del guilds[str(ctx.guild.id)]['DEFAULT_VOLUME']
                guilds[str(ctx.guild.id)]['DEFAULT_VOLUME'] = (new_volume / 100)
                await ctx.send(f":information_source: New default volume: **{new_volume}%**")
        else:
            if new_volume is None:
                await ctx.send(":information_source: Current default volume: **50%**")
            else:
                guilds[str(ctx.guild.id)] = {}
                guilds[str(ctx.guild.id)]['DEFAULT_VOLUME'] = (new_volume / 100)
                await ctx.send(f":information_source: New default volume: **{new_volume}%**")

        with open('guilds.json', 'w') as fp:
            json.dump(guilds, fp, indent=4)

def setup(bot):
    bot.add_cog(GuildSettings(bot))
