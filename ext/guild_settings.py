# Procbot Copyright (C) 2018 sirtezza451
# The full license can be found at master/LICENSE

import json

import discord
from discord.ext import commands

class GuildSettings:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(aliases=['settings'])
    @commands.guild_only()
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            subcommands = '`prefix` `default_volume`'
            await ctx.send(f':grey_exclamation: Please specify one of the following subcommands:\n{subcommands}')

    @setting.command()
    @commands.guild_only()
    async def prefix(self, ctx, new_prefix: str = None):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)

        if str(ctx.guild.id) in guilds:
            if new_prefix is None:
                await ctx.send(f":information_source: Current server prefix: **{guilds[str(ctx.guild.id)]['GUILD_PREFIX']}**")
            else:
                guilds[str(ctx.guild.id)]['GUILD_PREFIX'] = {}
                guilds[str(ctx.guild.id)]['GUILD_PREFIX'] = new_prefix
                await ctx.send(f":information_source: New server prefix: **{new_prefix}**")
        else:
            if new_prefix is None:
                await ctx.send(':information_source: Current server prefix: **.**')
            else:
                guilds[str(ctx.guild.id)]['GUILD_PREFIX'] = {}
                guilds[str(ctx.guild.id)]['GUILD_PREFIX'] = new_prefix
                await ctx.send(f":information_source: New server prefix: **{new_prefix}**")

        with open('guilds.json', 'w') as fp:
            json.dump(guilds, fp, indent=4)

    @setting.command()
    @commands.guild_only()
    async def default_volume(self, ctx, new_volume: int = None):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)

        if str(ctx.guild.id) in guilds:
            if new_volume is None:
                await ctx.send(f":information_source: Current default volume: **{round(guilds[str(ctx.guild.id)]['DEFAULT_VOLUME'] * 100)}%**")
            else:
                guilds[str(ctx.guild.id)]['DEFAULT_VOLUME'] = {}
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
