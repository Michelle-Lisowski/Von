'''
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
'''

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
            await ctx.send(':no_entry_sign: You must be the owner of me to use this command.')

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(':x: I could not find that extension.')

        else:
            print(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, ext: str = None):
        if ext is None:
            await ctx.send(':grey_exclamation: Please specify an extension to load.')
            return
        
        self.bot.load_extension(ext)
        success = discord.Embed()
        success.title = ':white_check_mark: Success!'
        success.description = f'Successfully loaded extension **{ext}**.'
        success.colour = 0x00ff00
        success.set_footer(text=datetime.datetime.now())
        await ctx.send(embed=success)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, ext: str = None):
        if ext is None:
            await ctx.send(':grey_exclamation: Please specify an extension to unload.')
            return

        self.bot.unload_extension(ext)
        success = discord.Embed()
        success.title = ':white_check_mark: Success!'
        success.description = f'Successfully unloaded extension **{ext}**.'
        success.colour = 0x00ff00
        success.set_footer(text=datetime.datetime.now())
        await ctx.send(embed=success)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, ext: str = None):
        if ext is None:
            await ctx.send(':grey_exclamation: Please specify an extension to reload.')
            return

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
