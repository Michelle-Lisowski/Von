# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join

import discord
from discord.ext import commands

from utils import set_token


class Von(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="?")
        self.remove_command("help")

    def run(self):
        token = set_token()

        try:
            self.loop.run_until_complete(self.login(token))
            self.loop.run_until_complete(self.connect())
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.logout())
        except discord.LoginFailure:
            print("Logging out due to unsuccessful connection...")
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
