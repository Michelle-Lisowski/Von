# Procbot Copyright (C) 2018 sirtezza451
# The full license can be found at master/LICENSE

import json

import discord
from discord.ext import commands

class GuildSettings:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group()
    @commands.guild_only()
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            subcommands = '`prefix`'
            await ctx.send(f':information_source: Please specify one of the following subcommands:\n{subcommands}')

    @setting.command()
    @commands.guild_only()
    async def prefix(self, ctx, new_prefix: str = None):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)

        if str(ctx.guild.id) in guilds:
            if new_prefix is None:
                await ctx.send(f":information_source: Current server prefix: **{guilds[str(ctx.guild.id)]['GUILD_PREFIX']}**")
                return
            else:
                guilds[str(ctx.guild.id)] = {}
                guilds[str(ctx.guild.id)]['GUILD_PREFIX'] = new_prefix
                await ctx.send(f":information_source: New server prefix: **{guilds[str(ctx.guild.id)]['GUILD_PREFIX']}**")
        else:
            if new_prefix is None:
                await ctx.send(':information_source: Current server prefix: **.**')
                return
            else:
                guilds[str(ctx.guild.id)] = {}
                guilds[str(ctx.guild.id)]['GUILD_PREFIX'] = new_prefix
                await ctx.send(f":information_source: New server prefix: **{guilds[str(ctx.guild.id)]['GUILD_PREFIX']}**")

        with open('guilds.json', 'w') as fp:
            json.dump(guilds, fp, indent=4)

def setup(bot):
    bot.add_cog(GuildSettings(bot))
