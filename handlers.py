# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


async def on_command_error(ctx, error):
    error = getattr(error, "original", error)

    if hasattr(ctx.command, "on_error"):
        pass

    elif isinstance(error, commands.CommandNotFound):
        pass

    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(error)

    elif isinstance(error, commands.CommandOnCooldown):
        cooldown_type = (
            str(error.cooldown.type).split("BucketType.")[1].replace("guild", "server")
        )
        await ctx.send(
            f":exclamation: Slow down! This {cooldown_type} can use command "
            f"`{ctx.command}` again after {round(error.retry_after)} seconds."
        )

    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send(
            f":exclamation: Command `{ctx.command}` can't be used in private messaging."
        )

    elif isinstance(error, commands.NotOwner):
        await ctx.send(":no_entry_sign: You must be the owner of bot to run command.")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(":no_entry_sign:" + error)

    elif isinstance(error, commands.MissingRequiredArgument):
        param = error.param.name.replace("_", " ")

        # cOrReCt GrAmMaR iS eXtReMeLy ImPoRtAnT iSnT iT
        if list(param)[0] in ["a", "e", "i", "o", "u"]:
            join = "an"
        else:
            join = "a"
        await ctx.send(f":grey_exclamation: Please specify {join} {param}.")

    elif isinstance(error, commands.CommandError):
        await ctx.send(error)


async def bad_argument(ctx, error):
    error = getattr(error, "original", error)

    if isinstance(error, commands.BadArgument):
        if str(ctx.command) == "roll":
            await ctx.send(":exclamation: Please specify a **number**.")
        elif str(ctx.command) == "gay" or "profile":
            await ctx.send(":exclamation: Member not found.")


def setup(bot):
    bot.add_listener(on_command_error)
    bot.add_handler(bad_argument, ["gay", "roll", "profile"])
