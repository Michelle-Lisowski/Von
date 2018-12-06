# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import json

import discord
from discord.ext import commands


class Settings:
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command can't be used in private messages.")

        elif isinstance(error, commands.CheckFailure):
            await ctx.send(
                "You require the **Manage Server** permission to use this command."
            )

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name != "settings default_volume":
                await ctx.send("Please specify either `True` or `False`.")
            else:
                await ctx.send("Please specify a number.")

    @commands.group(
        description="Group for commands that customise the bot's behaviour.",
        usage="settings [command] [arguments]",
        brief="settings prefix -",
    )
    @commands.guild_only()
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed()
            embed.title = "Server Settings"
            embed.colour = 0x0099FF

            try:
                prefix = self.bot.prefixes[str(ctx.guild.id)]["prefix"]
            except KeyError:
                prefix = "v!"
            cmds = []

            for cmd in self.settings.commands:
                cmds.append(prefix + cmd.qualified_name)

            cmds = "` `".join(cmds)
            embed.description = f"**`{cmds}`**"
            await ctx.send(embed=embed)

    @settings.command(
        description="Changes the bot's prefix.",
        usage="settings prefix [prefix]",
        brief="settings prefix -",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix: str = None):
        if prefix is None:
            await ctx.send("Please specify a new prefix.")
            return

        try:
            del self.bot.prefixes[str(ctx.guild.id)]["prefix"]
        except KeyError:
            pass

        try:
            self.bot.prefixes[str(ctx.guild.id)]["prefix"] = prefix
        except KeyError:
            self.bot.prefixes[str(ctx.guild.id)] = {}
            self.bot.prefixes[str(ctx.guild.id)]["prefix"] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(self.bot.prefixes, f, indent=4)
        await ctx.send(f":white_check_mark: Server prefix set to `{prefix}`.")

    @settings.command(
        description="Changes the default volume of music.",
        usage="settings default_volume [volume]",
        brief="settings default_volume 65",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def default_volume(self, ctx, volume: int = None):
        if volume is None:
            await ctx.send("Please specify a new default volume.")
            return
        elif not 0 < volume < 76:
            await ctx.send("Please specify a number between `1` and `75`.")
            return

        try:
            del self.bot.settings[str(ctx.guild.id)]["default_volume"]
        except KeyError:
            pass

        try:
            self.bot.settings[str(ctx.guild.id)]["default_volume"] = volume / 100
        except KeyError:
            self.bot.settings[str(ctx.guild.id)] = {}
            self.bot.settings[str(ctx.guild.id)]["default_volume"] = volume / 100

        with open("settings.json", "w") as f:
            json.dump(self.bot.settings, f, indent=4)
        await ctx.send(f":white_check_mark: Default volume set to `{volume}`.")

    @settings.command(
        description="Enables/disables sending the purge command's success message.",
        usage="settings purge_success [setting]",
        brief="settings purge_success False",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def purge_success(self, ctx, setting: bool = None):
        if setting is None:
            await ctx.send("Please specify either `True` or `False`.")
            return

        try:
            del self.bot.settings[str(ctx.guild.id)]["purge_success"]
        except KeyError:
            pass

        try:
            self.bot.settings[str(ctx.guild.id)]["purge_success"] = setting
        except KeyError:
            self.bot.settings[str(ctx.guild.id)] = {}
            self.bot.settings[str(ctx.guild.id)]["purge_success"] = setting

        with open("settings.json", "w") as f:
            json.dump(self.bot.settings, f, indent=4)

        if setting is True:
            await ctx.send(":white_check_mark: Purge success message enabled.")
        else:
            await ctx.send(":white_check_mark: Purge success message disabled.")

    @settings.command(
        description="Enables/disables sending member join and leave messages.",
        usage="settings auto_message [setting]",
        brief="settings auto_message False"
    )
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def auto_message(self, ctx, setting: bool = None):
        if setting is None:
            await ctx.send("Please specify either `True` or `False`.")
            return

        try:
            del self.bot.settings[str(ctx.guild.id)]["auto_message"]
        except KeyError:
            pass

        try:
            self.bot.settings[str(ctx.guild.id)]["auto_message"] = setting
        except KeyError:
            self.bot.settings[str(ctx.guild.id)] = {}
            self.bot.settings[str(ctx.guild.id)]["auto_message"] = setting

        with open("settings.json", "w") as f:
            json.dump(self.bot.settings, f, indent=4)

        if setting is True:
            await ctx.send(":white_check_mark: Member join/leave messages enabled.")
        else:
            await ctx.send(":white_check_mark: Member join/leave messages disabled.")

    @settings.command(
        description="Enables/disables automatically giving new members a role.",
        usage="settings auto_role [setting]",
        brief="settings auto_role False",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def auto_role(self, ctx, setting: bool = None):
        if setting is None:
            await ctx.send("Please specify either `True` or `False`.")
            return

        try:
            del self.bot.settings[str(ctx.guild.id)]["auto_role"]
        except KeyError:
            pass

        try:
            self.bot.settings[str(ctx.guild.id)]["auto_role"] = setting
        except KeyError:
            self.bot.settings[str(ctx.guild.id)] = {}
            self.bot.settings[str(ctx.guild.id)]["auto_role"] = setting

        with open("settings.json", "w") as f:
            json.dump(self.bot.settings, f, indent=4)

        if setting is True:
            await ctx.send(":white_check_mark: Auto-role feature enabled.")
        else:
            await ctx.send(":white_check_mark: Auto-role feature disabled.")

    @settings.command(
        description="Enables/disables votes for skipping songs.",
        usage="settings vote_skip [setting]",
        brief="settings vote_skip False",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def vote_skip(self, ctx, setting: bool = None):
        if setting is None:
            await ctx.send("Please specify either `True` or `False`.")
            return

        try:
            del self.bot.settings[str(ctx.guild.id)]["vote_skip"]
        except KeyError:
            pass

        try:
            self.bot.settings[str(ctx.guild.id)]["vote_skip"] = setting
        except KeyError:
            self.bot.settings[str(ctx.guild.id)] = {}
            self.bot.settings[str(ctx.guild.id)]["vote_skip"] = setting

        with open("settings.json", "w") as f:
            json.dump(self.bot.settings, f, indent=4)

        if setting is True:
            await ctx.send(":white_check_mark: Vote to skip feature enabled.")
        else:
            await ctx.send(":white_check_mark: Vote to skip feature disabled.")

    @settings.command(
        description="Enables/disables votes for clearing playlists.",
        usage="settings vote_clear [setting]",
        brief="settings vote_clear False",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def vote_clear(self, ctx, setting: bool = None):
        if setting is None:
            await ctx.send("Please specify either `True` or `False`.")
            return

        try:
            del self.bot.settings[str(ctx.guild.id)]["vote_clear"]
        except KeyError:
            pass

        try:
            self.bot.settings[str(ctx.guild.id)]["vote_clear"] = setting
        except KeyError:
            self.bot.settings[str(ctx.guild.id)] = {}
            self.bot.settings[str(ctx.guild.id)]["vote_clear"] = setting

        with open("settings.json", "w") as f:
            json.dump(self.bot.settings, f, indent=4)

        if setting is True:
            await ctx.send(":white_check_mark: Vote to clear feature enabled.")
        else:
            await ctx.send(":white_check_mark: Vote to clear feature disabled.")


def setup(bot):
    bot.add_cog(Settings(bot))
