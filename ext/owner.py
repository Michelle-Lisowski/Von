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

import discord
from discord.ext import commands

class Owner:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, ext: str):
        try:
            self.bot.load_extension(ext)
        except Exception as e:
            error = discord.Embed()
            error.title = ':x: Error!'
            error.description = f'```{e}```'
            error.colour = 0xff0000
            error.set_footer(text=datetime.datetime.now())
            await ctx.send(embed=error)
        else:
            success = discord.Embed()
            success.title = ':white_check_mark: Success!'
            success.description = f'Successfully loaded **{ext}**.'
            success.colour = 0x00ff00
            success.set_footer(text=datetime.datetime.now())
            await ctx.send(embed=success)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, ext: str):
        try:
            self.bot.unload_extension(ext)
        except Exception as e:
            error = discord.Embed()
            error.title = ':x: Error!'
            error.description = f'```{e}```'
            error.colour = 0xff0000
            error.set_footer(text=datetime.datetime.now())
            await ctx.send(embed=error)
        else:
            success = discord.Embed()
            success.title = ':white_check_mark: Success!'
            success.description = f'Successfully unloaded **{ext}**.'
            success.colour = 0x00ff00
            success.set_footer(text=datetime.datetime.now())
            await ctx.send(embed=success)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, ext: str):
        try:
            self.bot.unload_extension(ext)
            self.bot.load_extension(ext)
        except Exception as e:
            error = discord.Embed()
            error.title = ':x: Error!'
            error.description = f'```{e}```'
            error.colour = 0xff0000
            error.set_footer(text=datetime.datetime.now())
            await ctx.send(embed=error)
        else:
            success = discord.Embed()
            success.title = ':white_check_mark: Success!'
            success.description = f'Successfully reloaded **{ext}**.'
            success.colour = 0x00ff00
            success.set_footer(text=datetime.datetime.now())
            await ctx.send(embed=success)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def logout(self, ctx):
        await self.bot.logout()

def setup(bot):
    bot.add_cog(Owner(bot))
