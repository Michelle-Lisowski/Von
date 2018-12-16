# -*- coding: utf-8 -*-

import asyncio
import sys
from os import listdir
from os.path import isfile, join

try:
    import discord
    from aiohttp import ClientConnectorError
    from discord.ext import commands

    import psutil
    import utils
except (ImportError, ModuleNotFoundError):
    if sys.argv[0] != "setup.py":
        print(
            "Some required dependencies are missing.",
            "Please run the setup to install these.",
        )
        sys.exit(1)
except SyntaxError:
    print(
        "A syntax error occurred while importing",
        "the required dependencies. This is likely",
        "because of an unsupported Python version,",
        "such as Python 2.x or Python 3.3 or lower.",
    )
    sys.exit(1)


class Von(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.get_prefix)
        self.remove_command("help")

        self.custom = utils.get_custom_settings()
        self.process = psutil.Process()

        self.discordpy_version = discord.__version__
        self.python_version = sys.version.split(" (")[0]

    def add_handler(self, coro, command: str):
        command = self.get_command(command)

        if command is None:
            raise commands.CommandNotFound(
                "add_handler: A command with the specified name wasn't found."
            )

        if not asyncio.iscoroutinefunction(coro):
            raise discord.ClientException(
                "add_handler: The specified function must be a coroutine."
            )

        command.on_error = coro
        return coro

    def run(self):
        token = utils.set_token()

        try:
            self.loop.run_until_complete(self.login(token))
            self.loop.run_until_complete(self.connect())
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.logout())
        except (discord.LoginFailure, discord.HTTPException, ClientConnectorError):
            print("Logging out due to unsuccessful connection...")
            self.loop.run_until_complete(self.logout())
        except (discord.GatewayNotFound, discord.ConnectionClosed):
            print("Logging out due to unsuccessful gateway connection...")
            self.loop.run_until_complete(self.logout())
        finally:
            self.loop.close()

    async def on_ready(self):
        print("Ready: {0} (ID: {0.id})".format(self.user))
        await self.change_presence(activity=discord.Game(name="with code"))

        for command in [
            f.replace(".py", "")
            for f in listdir("command")
            if isfile(join("command", f))
        ]:
            try:
                self.load_extension(f"command.{command}")
            except (discord.ClientException, ModuleNotFoundError):
                print(f"Failed to load command {command}")

        # Loading exception handlers as an extension allows for easy reloading
        try:
            self.load_extension("handlers")
        except (discord.ClientException, ModuleNotFoundError):
            print("Failed to load exception handlers")

        # Loading custom checks as an extension allows for easy reloading
        try:
            self.load_extension("checks")
        except (discord.ClientException, ModuleNotFoundError):
            print("Failed to load custom checks")

    async def on_message(self, message):
        if message.content.startswith("?prefix"):
            if message.guild is None:
                return await message.channel.send(
                    ":exclamation: Command `prefix` can't be used in private messaging."
                )

            embed = discord.Embed()
            embed.colour = 0x0099FF
            embed.title = self.user.name
            prefix = await self.get_prefix(message)

            embed.description = f"The prefix in this server is `{prefix}`."
            await message.channel.send(embed=embed)
        await self.process_commands(message)

    async def get_prefix(self, message):
        try:
            prefix = self.custom[str(message.guild.id)]["PREFIX"]
        except (KeyError, AttributeError):
            prefix = "?"
        return prefix
