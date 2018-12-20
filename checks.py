# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


async def is_enabled(ctx):
    try:
        disabled_commands = ctx.bot.custom[str(ctx.guild.id)]["DISABLED_COMMANDS"]
    # An AttributeError would happen in DMs, since the guild attribute doesn't exist
    except (KeyError, AttributeError):
        disabled_commands = []

    if str(ctx.command) in disabled_commands:
        raise commands.DisabledCommand(
            f":exclamation: Command `{ctx.command}` has been disabled."
        )
    return True


async def is_connected(ctx):
    if not ctx.voice_client:
        if str(ctx.command) == "play":
            try:
                await ctx.author.voice.channel.connect()
            except AttributeError:
                raise commands.CommandError(
                    ":grey_exclamation: Please join a voice channel first."
                )
    else:
        if not ctx.author.voice:
            raise commands.CommandError(
                ":grey_exclamation: Please join a voice channel first."
            )
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            raise commands.CommandError(
                ":grey_exclamation: Please join the same voice channel as me."
            )
    return True


async def is_playing(ctx):
    if not ctx.voice_client or not ctx.voice_client.is_playing():
        raise commands.CommandError(":grey_exclamation: No music is currently playing.")
    elif ctx.voice_client.is_paused():
        raise commands.CommandError(
            ":grey_exclamation: The currently playing music has been paused."
        )
    return True


def setup(bot):
    bot.add_check(is_enabled)
    bot.add_command_check(is_playing, ["skip", "stop", "volume"])
    bot.add_command_check(is_connected, ["play", "skip", "stop", "volume"])
