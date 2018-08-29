# Procbot Copyright (C) 2018 sirtezza451
# The full license can be found at master/LICENSE

import datetime
import sys
import traceback

import discord
from discord.ext import commands

class Owner:
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(':x: You must be the owner of me to use this command.')

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(':x: I could not find that extension.')

        else:
            print(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)            

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, ext: str):
        self.bot.load_extension(ext)
        success = discord.Embed()
        success.title = ':white_check_mark: Success!'
        success.description = f'Successfully loaded extension **{ext}**.'
        success.colour = 0x00ff00
        success.set_footer(text=datetime.datetime.now())
        await ctx.send(embed=success)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, ext: str):
        self.bot.unload_extension(ext)
        success = discord.Embed()
        success.title = ':white_check_mark: Success!'
        success.description = f'Successfully unloaded extension **{ext}**.'
        success.colour = 0x00ff00
        success.set_footer(text=datetime.datetime.now())
        await ctx.send(embed=success)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, ext: str):
        self.bot.unload_extension(ext)
        self.bot.load_extension(ext)
        success = discord.Embed()
        success.title = ':white_check_mark: Success!'
        success.description = f'Successfully reloaded extension **{ext}**.'
        success.colour = 0x00ff00
        success.set_footer(text=datetime.datetime.now())
        await ctx.send(embed=success)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def logout(self, ctx):
        await self.bot.logout()

def setup(bot):
    bot.add_cog(Owner(bot))
