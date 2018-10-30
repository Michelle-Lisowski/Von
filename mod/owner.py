# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


class Owner:
    """
    Command module for owner commands.

    These commands can only be used by the owner
    of the bot, and allow for custom command modules.

    List of commands:
    ```
    v!load
    v!unload
    v!reload
    ```
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, mod: str = None):
        if mod is None:
            await ctx.send(":grey_exclamation: Please specify a module.")
            return

        try:
            self.bot.load_extension(mod)
        except:
            await ctx.send(f":x: An error occured while loading `{mod}`.")
        else:
            await ctx.send(f":white_check_mark: `{mod}` loaded.")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, mod: str = None):
        if mod is None:
            await ctx.send(":grey_exclamation: Please specify a module.")
            return

        try:
            self.bot.load_extension(mod)
        except:
            await ctx.send(f":x: An error occured while unloading `{mod}`.")
        else:
            await ctx.send(f":white_check_mark: `{mod}` unloaded.")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, mod: str = None):
        if mod is None:
            await ctx.send(":grey_exclamation: Please specify a module.")
            return

        try:
            self.bot.unload_extension(mod)
            self.bot.load_extension(mod)
        except:
            await ctx.send(f":x: An error occured while reloading `{mod}`.")
        else:
            await ctx.send(f":white_check_mark: `{mod}` reloaded.")

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Owner(bot))

