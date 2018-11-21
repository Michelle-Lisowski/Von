# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import json

import discord
from discord.ext import commands


class Settings:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed()
            embed.title = "Server Settings"
            embed.colour = 0x0099FF

            try:
                prefix = self.bot.prefixes[str(ctx.guild.id)]["prefix"]
            except AttributeError:
                raise commands.NoPrivateMessage
            cmds = []

            for cmd in self.settings.commands:
                cmds.append(prefix + cmd.qualified_name)

            cmds = "` `".join(cmds)
            embed.description = f"**`{cmds}`**"
            await ctx.send(embed=embed)

    @settings.command()
    @commands.guild_only()
    async def prefix(self, ctx, prefix: str = None):
        if prefix is None:
            await ctx.send("Please specify a new prefix.")
            return

        del self.bot.prefixes[str(ctx.guild.id)]["prefix"]
        self.bot.prefixes[str(ctx.guild.id)]["prefix"] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(self.bot.prefixes, f, indent=4)

        await ctx.send(f":white_check_mark: Server prefix set to `{prefix}`.")

    @settings.command()
    @commands.guild_only()
    async def default_volume(self, ctx, volume: int = None):
        if volume is None:
            await ctx.send("Please specify a new default volume.")
            return

        try:
            del self.bot.settings[str(ctx.guild.id)]["default_volume"]
        except KeyError:
            pass
        self.bot.settings[str(ctx.guild.id)]["default_volume"] = volume / 100

        with open("settings.json", "w") as f:
            json.dump(self.bot.settings, f, indent=4)

        await ctx.send(f":white_check_mark: Default volume set to `{volume}`.")

    @settings.command()
    @commands.guild_only()
    async def purge_success(self, ctx, setting: bool = None):
        if setting is None:
            await ctx.send("Please specify either `True` or `False`.")
            return

        try:
            del self.bot.settings[str(ctx.guild.id)]["purge_success"]
        except KeyError:
            pass
        self.bot.settings[str(ctx.guild.id)]["purge_success"] = setting

        with open("settings.json", "w") as f:
            json.dump(self.bot.settings, f, indent=4)

        if setting is True:
            await ctx.send(":white_check_mark: Purge success message enabled.")
        else:
            await ctx.send(":white_check_mark: Purge success message disabled.")

    @settings.command()
    @commands.guild_only()
    async def auto_message(self, ctx, setting: bool = None):
        if setting is None:
            await ctx.send("Please specify either `True` or `False`.")
            return

        try:
            del self.bot.settings[str(ctx.guild.id)]["auto_message"]
        except KeyError:
            pass
        self.bot.settings[str(ctx.guild.id)]["auto_message"] = setting

        with open("settings.json", "w") as f:
            json.dump(self.bot.settings, f, indent=4)

        if setting is True:
            await ctx.send(":white_check_mark: Member join/leave messages enabled.")
        else:
            await ctx.send(":white_check_mark: Member join/leave messages disabled.")

    @settings.command()
    @commands.guild_only()
    async def auto_role(self, ctx, setting: bool = None):
        if setting is None:
            await ctx.send("Please specify either `True` or `False`.")
            return

        try:
            del self.bot.settings[str(ctx.guild.id)]["auto_role"]
        except KeyError:
            pass
        self.bot.settings[str(ctx.guild.id)]["auto_role"] = setting

        with open("settings.json", "w") as f:
            json.dump(self.bot.settings, f, indent=4)

        if setting is True:
            await ctx.send(":white_check_mark: Auto-role feature enabled.")
        else:
            await ctx.send(":white_check_mark: Auto-role feature disabled.")


def setup(bot):
    bot.add_cog(Settings(bot))
