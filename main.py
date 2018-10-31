# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import json
import os
import sys
from os import listdir
from os.path import isfile, join

import discord
from discord.ext import commands

PYTHON_OK = sys.version_info >= (3, 6, 0)


class Von(commands.Bot):
    """
    Instance of `discord.ext.commands.Bot`

    This allows to pass in custom functions
    to the `Bot` class itself, meaning that
    functions can simply be called in a 
    command module without imports. For
    example, `Von.my_function(arg)` can be
    called with `self.bot.my_function(arg)`
    within the code of a command module.
    """

    def region_clean(self, guild):
        """
        Returns a clean string of the voice
        region of the guild argument passed.
        """

        s = str(guild.region)
        if "-" in s:
            sn = s.replace("-", " ")

            if "vip" in sn:
                sr = sn.replace("vip ", "")
            if "eu" in sn:
                sr = sn.replace("eu", "EU")
            if "us" in sn:
                sr = sn.replace("us", "US")

            sl = sr.split(" ")

            sf = f"{sl[0]} {sl[1].capitalize()}"
        elif s == "hongkong":
            sf = "Hong Kong"
        elif s == "southafrica":
            sf = "South Africa"
        else:
            sf = s.capitalize()
        return sf

    def status_cap(self, status):
        """
        Returns a capitalised string of the
        status argument passed.

        By default, the string of a member's
        status would be `offline`, `dnd`, `idle`
        or `online`.

        Returns:
            "Do Not Disturb"
            str(status).capitalize()
        """
        if status == discord.Status.dnd:
            s = "Do Not Disturb"
        else:
            s = str(status).capitalize()
        return s

    def level_cap(self, level):
        """
        Returns a capitalised string of the
        verification level argument passed.

        Returns:
            "None"
            "Low"
            "Medium"
            "High"
            "Extreme"
        """

        return str(level).capitalize()

    def atype_str(self, activity):
        """
        Returns a type string of the activity
        argument passed.

        By default, `discord.Member.activity.type`
        returns an integer.

        Returns:
            "Playing"
            "Streaming"
            "Listening"
            "Watching"
        """

        if activity.type == 0:
            atype = "Playing"
        elif activity.type == 1:
            atype = "Streaming"
        elif activity.type == 2:
            atype = "Listening"
        elif activity.type == 3:
            atype = "Watching"
        return atype

    async def on_ready(self):
        """
        Logs successful connection and sets
        activity with type `Playing`
        """

        print(
            "Von's awake.\n" f"Username: {str(self.user)}\n" f"ID: {str(self.user.id)}"
        )

        await self.change_presence(
            activity=discord.Streaming(
                name=f"with {len(self.users)} viewers!", url="https://twitch.tv/kraken"
            )
        )

    async def on_message(self, message):
        """
        Processes commands and sends prefix upon plain mention

        When a message is received containing just a bot mention,
        sends a message that alerts the user of the current guild
        prefix.

        `Von.process_commands(message)` is run since commands won't
        be processed by default in a custom `discord.on_message`
        event.
        """

        if message.content == self.user.mention:
            embed = discord.Embed()
            embed.colour = 0x0099FF
            embed.description = "The prefix in this server is `v!`."
            await message.channel.send(embed=embed)

        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        """
        Global command error handler
        
        This can be overridden by module-specific
        handlers, and even command-specific handlers.
        """

        error = getattr(error, "original", error)

        if isinstance(error, commands.CommandNotFound):
            return

        elif hasattr(ctx.command, "on_error"):
            return

        elif hasattr(ctx.cog, f"_{ctx.cog.__class__.__name__}__error"):
            return

        else:
            await ctx.send(f":x: An error occured!\n```{error}```")

    async def on_member_join(self, member):
        """
        Auto-role feature

        Finds the 'Member' role and creates it
        if it doesn't exist, then gives it to
        the member.
        """

        role = discord.utils.get(member.guild.roles, name="Member")

        if role is None:
            role = await member.guild.create_role(name="Member", hoist=True)

        await member.add_roles(role)


def main(bot):
    """
    Runs Von and loads command modules

    Checks if the user's Python version
    supports Von; aborts launch if it doesn't.
    As an extra precaution, the existence of
    `settings.json` is also checked.

    When the above requirements are met,
    `settings.json` is read. The `DISCORD_TOKEN`
    key is used as the bot token; if a `KeyError`
    is raised, the token will then be set by the
    second command line argument.
    """

    if not PYTHON_OK:
        version = "{0.major}.{0.minor}.{0.micro}".format(sys.version_info)
        print(
            "Von requires Python 3.6.0 or above. You currently have "
            f"Python {version}. Please update Python to run Von!"
        )
        sys.exit(1)

    try:
        with open("settings.json") as fp:
            settings = json.load(fp)
    except FileNotFoundError:
        print(
            "Settings file not found. Please create a file in the root "
            "directory named 'settings.json' and make sure it contains "
            "an empty dictionary."
        )
        sys.exit(1)

    if len(sys.argv) > 1:
        if settings["DISCORD_TOKEN"]:
            del settings["DISCORD_TOKEN"]

    try:
        token = settings["DISCORD_TOKEN"]
    except KeyError:
        token = sys.argv[1]
        if token is None:
            print(
                "Please specify a bot token as a command line argument. "
                "Make sure to use the following format:\n"
                "python [script] [token]"
            )
            sys.exit(1)
        else:
            settings["DISCORD_TOKEN"] = token

    with open("settings.json", "w") as fp:
        json.dump(settings, fp, indent=4)

    for mod in [f.replace(".py", "") for f in listdir("mod") if isfile(join("mod", f))]:
        try:
            bot.load_extension(f"mod.{mod}")
        except (discord.ClientException, ModuleNotFoundError):
            print(f"Failed to load {mod}")
        else:
            print(f"Successfully loaded {mod}")

    try:
        bot.run(settings["DISCORD_TOKEN"])
    except KeyboardInterrupt:
        sys.exit(1)
    except discord.ClientException:
        print("Invalid Discord token. Please pass in a valid token and try again.")
        sys.exit(1)


if __name__ == "__main__":
    bot = Von("v!")
    bot.remove_command("help")
    main(bot)
