# Procbot Copyright (C) 2018 sirtezza451
# The full license can be found at master/LICENSE

import json
import random
import sys
import traceback

import discord
from discord import utils
from discord.ext import commands

from src.colours import DISCORD_COLOURS

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

        elif isinstance(error, MissingPermissions):
            await ctx.send(':no_entry_sign: You require the `Staff` role to use this command.')

        elif isinstance(error, commands.BadArgument):
            await ctx.send(':x: Please specify a **whole number** for the new default volume.')

        else:
            print(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    async def is_guild_owner(self, ctx):
        return ctx.author.id == ctx.guild.owner.id
        
    @commands.group(aliases=['settings'])
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            subcommands = '`prefix` `default_volume`'
            await ctx.send(f':grey_exclamation: Please specify one of the following subcommands:\n{subcommands}')

    @setting.command()
    @commands.guild_only()
    @commands.check(is_guild_owner)
    async def prefix(self, ctx, new_prefix: str = None):
        staff_role = utils.get(ctx.guild.roles, name='Staff')
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)

        role_colour = random.choice(DISCORD_COLOURS)
        if staff_role is None:
            staff_role = await ctx.guild.create_role(name='Staff', colour=role_colour, hoist=True, reason='Role for server staff/moderators.')

        if not staff_role in ctx.author.roles:
            raise MissingPermissions
        else:
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
    @commands.check(is_guild_owner)
    async def default_volume(self, ctx, new_volume: int = None):
        staff_role = utils.get(ctx.guild.roles, name='Staff')
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)

        role_colour = random.choice(DISCORD_COLOURS)
        if staff_role is None:
            staff_role = await ctx.guild.create_role(name='Staff', colour=role_colour, hoist=True, reason='Role for server staff/moderators.')

        if not staff_role in ctx.author.roles:
            raise MissingPermissions
        else:
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
