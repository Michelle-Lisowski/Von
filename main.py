# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import json
import os
import random
import sys
import time
import traceback
from os import listdir
from os.path import isfile, join

import aiohttp
import discord
from discord.ext import commands


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
        self.session = aiohttp.ClientSession(loop=self.loop)

        with open("experience.json") as f:
            self.experience = json.load(f)

        with open("prefixes.json") as f:
            self.prefixes = json.load(f)

        with open("settings.json") as f:
            self.settings = json.load(f)

        for mod in [
            f.replace(".py", "") for f in listdir("mod") if isfile(join("mod", f))
        ]:
            try:
                self.load_extension(f"mod.{mod}")
            except:
                print(f"Failed to load extension {mod}.", file=sys.stderr)
                traceback.print_exc()

    async def on_guild_channel_delete(self, channel):
        if channel.name == "welcome":
            try:
                await channel.guild.create_text_channel(name="welcome")
            except (discord.Forbidden, discord.HTTPException):
                pass

        elif channel.name == "logs":
            try:
                await channel.guild.create_role(name="logs")
            except (discord.Forbidden, discord.HTTPException):
                pass

    async def on_guild_role_delete(self, role):
        if role.name == "Muted":
            try:
                await role.guild.create_role(name="Muted")
            except (discord.Forbidden, discord.HTTPException):
                pass

        elif role.name == "Member":
            try:
                colour = random.randint(0x000000, 0xFFFFFF)
                await role.guild.create_role(name="Member", colour=colour)
            except (discord.Forbidden, discord.HTTPException):
                pass

    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name="Member")
        channel = discord.utils.get(member.guild.text_channels, name="welcome")

        try:
            send_message = self.settings[str(member.guild.id)]["auto_message"]
            add_role = self.settings[str(member.guild.id)]["auto_role"]
        except KeyError:
            self.settings[str(member.guild.id)] = {}
            self.settings[str(member.guild.id)]["auto_message"] = True
            self.settings[str(member.guild.id)]["auto_role"] = True

            send_message = self.settings[str(member.guild.id)]["auto_message"]
            add_role = self.settings[str(member.guild.id)]["auto_role"]

            with open("settings.json", "w") as f:
                json.dump(self.settings, f, indent=4)

        if add_role is True and role is None:
            return
        elif channel is None:
            return

        try:
            if add_role is True:
                await member.add_roles(role)

            if send_message is True:
                await channel.send(
                    f"Welcome to **{member.guild}**, {member.mention}! :tada::hugging:"
                )
        except (discord.Forbidden, discord.HTTPException):
            pass

    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome")

        try:
            send_message = self.settings[str(member.guild.id)]["auto_message"]
        except KeyError:
            self.settings[str(member.guild.id)] = {}
            self.settings[str(member.guild.id)]["auto_message"] = True
            send_message = self.settings[str(member.guild.id)]["auto_message"]

        if channel is None:
            return

        try:
            if send_message is True:
                await channel.send(
                    f"We're sad to see you leave, **<@{member.id}>**... :frowning2:"
                )
        except (discord.Forbidden, discord.HTTPException):
            pass

    async def on_member_ban(self, guild, user):
        audit_ban = discord.AuditLogAction.ban
        channel = discord.utils.get(guild.text_channels, name="logs")

        if channel is None:
            return

        try:
            async for ban in guild.audit_logs(limit=1, action=audit_ban):
                embed = discord.Embed()
                embed.title = "Ban"
                embed.colour = 0x0099FF

                embed.add_field(name="Member", value=ban.target)
                embed.add_field(name="Member ID", value=ban.target.id)
                embed.add_field(name="Responsible Moderator", value=ban.user)
                embed.add_field(name="Time", value=ban.created_at)
                embed.add_field(name="Reason", value=ban.reason)

                try:
                    await channel.send(embed=embed)
                except (discord.Forbidden, discord.HTTPException):
                    pass
        except (discord.Forbidden, discord.HTTPException):
            pass

    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.CommandNotFound):
            return

    async def on_ready(self):
        if not hasattr(self, "uptime"):
            self.uptime = time.time()

        print("Ready: {0} (ID: {0.id})".format(self.user))

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

        if message.content.startswith("v!prefix"):
            if not message.guild:
                await message.channel.send("This command can't be used in private messages.")
                return

            embed = discord.Embed()
            embed.colour = 0x0099FF

            try:
                prefix = self.prefixes[str(message.guild.id)]["prefix"]
            except KeyError:
                self.prefixes[str(message.guild.id)] = {}
                self.prefixes[str(message.guild.id)]["prefix"] = "v!"
                prefix = self.prefixes[str(message.guild.id)]["prefix"]

                with open("prefixes.json", "w") as f:
                    json.dump(self.prefixes, f, indent=4)            

            embed.title = self.user.name
            embed.description = f"The prefix in this server is `{prefix}`."

            try:
                await message.channel.send(embed=embed)
            except (discord.Forbidden, discord.HTTPException):
                pass

        await self.add_experience(message.author)
        await self.level_up(message.author, message.channel)
        await self.process_commands(message)

        with open("experience.json", "w") as f:
            json.dump(self.experience, f, indent=4)

    async def on_message_edit(self, before, after):
        if not before.guild:
            return

        try:
            prefix = self.prefixes[str(before.guild.id)]["prefix"]
        except KeyError:
            self.prefixes[str(before.guild.id)] = {}
            self.prefixes[str(before.guild.id)]["prefix"] = "v!"
            prefix = self.prefixes[str(before.guild.id)]["prefix"]

            with open("prefixes.json", "w") as f:
                json.dump(self.prefixes, f, indent=4)

        if prefix in before.content:
            if before.content == prefix:
                await self.process_commands(after)
            else:
                pass
        else:
            await self.process_commands(after)

    async def mute(self, member):
        role = discord.utils.get(member.guild.roles, name="Muted")
        channels = [channel for channel in member.guild.channels]

        if role is None:
            raise commands.CommandError(f"Muting <@{member.id}> failed.")

        for channel in channels:
            try:
                await channel.set_permissions(role, connect=False, send_messages=False)
            except (discord.Forbidden, discord.HTTPException):
                raise commands.CommandError(f"Muting <@{member.id}> failed.")

        if role in member.roles:
            raise commands.CommandError(f"<@{member.id}> has already been muted.")

        try:
            await member.add_roles(role)
        except (discord.Forbidden, discord.HTTPException):
            raise commands.CommandError(f"Muting <@{member.id}> failed.")

    async def add_experience(self, member):
        if member.bot:
            return

        try:
            self.experience[str(member.id)]["experience"] += 2
        except KeyError:
            self.experience[str(member.id)] = {}
            self.experience[str(member.id)]["experience"] = 2
            self.experience[str(member.id)]["level"] = 1

    async def level_up(self, member, channel):
        if member.bot:
            return

        experience = self.experience[str(member.id)]["experience"]
        before = self.experience[str(member.id)]["level"]
        after = int(experience ** (1 / 4))

        if before < after:
            embed = discord.Embed()
            embed.colour = 0x0099FF
            embed.title = f"{member.name} has levelled up!"

            embed.add_field(name="Experience", value=f"{experience} XP")
            embed.add_field(name="Level", value=after)
            self.experience[str(member.id)]["level"] = after
            
            with open("experience.json", "w") as f:
                json.dump(self.experience, f, indent=4)

            try:
                await channel.send(embed=embed)
            except (discord.Forbidden, discord.HTTPException):
                pass
