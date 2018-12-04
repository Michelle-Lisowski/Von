# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import json
import typing

import discord
from discord.ext import commands


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command can't be used in private messages.")

        elif isinstance(error, commands.CheckFailure):
            await ctx.send(
                "You require the **Manage Messages** permission to run this command."
            )

        elif isinstance(error, commands.BadArgument):
            await ctx.send("Member not found.")

        elif isinstance(error, commands.CommandError):
            await ctx.send(error)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Please specify a member.")
        elif member.id == ctx.author.id:
            await ctx.send("Why would you want to mute yourself?")
        elif member.id == self.bot.user.id:
            await ctx.send("Why would you want to ban me?")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send("Maybe try muting someone with a lower role than yours.")
        else:
            embed = discord.Embed()
            embed.title = "Mute"
            embed.colour = 0x0099FF

            await self.bot.mute(member)
            embed.add_field(name="Member", value=str(member))
            embed.add_field(name="Member ID", value=member.id)
            embed.add_field(name="Muted By", value=str(ctx.author))
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Please specify a member.")
        elif member.id == ctx.author.id:
            await ctx.send(
                "You're using this command, so you were never muted in the first place!"
            )
        elif member.id == self.bot.user.id:
            await ctx.send(
                "I'm reponding to this command, so I was never muted in the first place!"
            )
        elif member.top_role >= ctx.author.top_role:
            await ctx.send("Maybe try unmuting someone with a lower role than yorus.")
        else:
            role = discord.utils.get(ctx.guild.roles, name="Muted")

            if not role in member.roles or role is None:
                await ctx.send(f"<@{member.id}> was never muted.")
                return

            embed = discord.Embed()
            embed.title = "Unmute"
            embed.colour = 0x0099FF

            try:
                await member.remove_roles(role)
            except (discord.Forbidden, discord.HTTPException):
                await ctx.send(f"Muting <@{member.id}> failed.")
                return

            embed.add_field(name="Member", value=str(member))
            embed.add_field(name="Member ID", value=member.id)
            embed.add_field(name="Unmuted By", value=str(ctx.author))
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(
        self, ctx, member: typing.Optional[discord.Member] = None, number: int = None
    ):
        if member is None:
            members = [member for member in ctx.guild.members]
        else:
            members = [member]

        if number is None:
            await ctx.send("Please specify a number.")
            return

        counter = 0

        async for message in ctx.channel.history():
            for member in members:
                if message.author.id == member.id:
                    if counter < number:
                        await message.delete()
                        counter += 1
                    else:
                        break

        try:
            purge_success = self.bot.settings[str(ctx.guild.id)]["purge_success"]
        except KeyError:
            try:
                self.bot.settings[str(ctx.guild.id)]["purge_success"] = True
            except KeyError:
                self.bot.settings[str(ctx.guild.id)] = {}
                self.bot.settings[str(ctx.guild.id)]["purge_success"] = True
            purge_success = self.bot.settings[str(ctx.guild.id)]["purge_success"]

            with open("settings.json", "w") as f:
                json.dump(self.bot.settings, f, indent=4)

        if purge_success is True:
            await ctx.send(
                f":white_check_mark: Successfully deleted {counter} messages."
            )
        else:
            pass


def setup(bot):
    bot.add_cog(Moderation(bot))
