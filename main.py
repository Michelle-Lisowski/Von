# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import json
import os
import sys
import time
import traceback
from os import listdir
from os.path import isfile, join

import discord
from discord.ext import commands

import aiohttp


def prefix_callable(bot, message):
    if message.guild is None:
        prefix = "v!"
    else:
        try:
            prefix = bot.prefixes[str(message.guild.id)]["prefix"]
        except KeyError:
            bot.prefixes[str(message.guild.id)] = {}
            bot.prefixes[str(message.guild.id)]["prefix"] = "v!"
            prefix = bot.prefixes[str(message.guild.id)]["prefix"]

            with open("prefixes.json", "w") as f:
                json.dump(bot.prefixes, f, indent=4)
    return prefix


class Von(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=prefix_callable)
        self.remove_command("help")
        
        with open("prefixes.json") as f:
            self.prefixes = json.load(f)
        self.session = aiohttp.ClientSession(loop=self.loop)

        for mod in [f.replace(".py", "") for f in listdir("mod") if isfile(join("mod", f))]:
            try:
                self.load_extension(f"mod.{mod}")
            except:
                print(f"Failed to load extension {mod}.", file=sys.stderr)
                traceback.print_exc()

    async def on_command(self, ctx):
        with open("prefixes.json") as f:
            self.prefixes = json.load(f)    

    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name="Member")
        channel = discord.utils.get(member.guild.text_channels, name="welcome")

        if role is None:
            role = await member.guild.create_role(name="Member", hoist=True)

        if channel is None:
            channel = await member.guild.create_text_channel(name="welcome")

        await member.add_roles(role)
        await channel.send(
            f"Welcome to **{member.guild}**, {member.mention}! :tada::hugging:"
        )

    async def on_member_ban(self, guild, user):
        audit_ban = discord.AuditLogAction.ban
        channel = discord.utils.get(guild.text_channels, name="logs")

        if channel is None:
            channel = await guild.create_text_channel(name="logs")

        async for ban in guild.audit_logs(limit=1, action=audit_ban):
            embed = discord.Embed()
            embed.title = "Ban"
            embed.colour = 0x0099FF

            embed.add_field(name="Member", value=ban.user)
            embed.add_field(name="Member ID", value=ban.user.id)
            embed.add_field(name="Reason", value=ban.reason)
            embed.add_field(name="Responsible Moderator", value=ban.user)
            embed.add_field(name="Time", value=ban.created_at)
            await channel.send(embed=embed)               

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return
        elif hasattr(ctx.cog, f"_{ctx.cog.__class__.__name__}__error"):
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command can't be used in private messages.")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("Sorry. This command is disabled and can't be used.")
        else:
            print(f"In {ctx.command.qualified_name}:", file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print(f"{error.original.__class__.__name__}: {error.original}", file=sys.stderr)                

    async def on_ready(self):
        if not hasattr(self, "uptime"):
            self.uptime = time.time()

        print(f"Ready: {self.user} (ID: {self.user.id})")

        await self.change_presence(
            activity=discord.Streaming(
                name=f"with {len(self.users)} viewers!", url="https://twitch.tv/kraken"
            )
        )

    async def on_resumed(self):
        print("Resumed...")

    async def on_message(self, message):
        if message.author.bot:
            return

        with open("prefixes.json") as f:
            self.prefixes = json.load(f)

        if message.content.startswith("v!prefix"):
            embed = discord.Embed()
            embed.colour = 0x0099FF

            prefix = self.prefixes[str(message.guild.id)]["prefix"]
            embed.description = f"The prefix in this server is `{prefix}`"
            await message.channel.send(embed=embed)
        await self.process_commands(message)
