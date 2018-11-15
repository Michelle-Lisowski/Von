# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


class Admin:
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.CheckFailure):
            if str(ctx.command) == "kick":
                await ctx.send(
                    "You require the **Kick Members** permission to run this command."
                )
            elif str(ctx.command) == "ban":
                await ctx.send(
                    "You require the **Ban Members** permission to run this command."
                )

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Please specify a member.")
        elif member.id == ctx.author.id:
            await ctx.send("Why would you want to kick yourself?")
        elif member.id == self.bot.user.id:
            await ctx.send("Why would you want to kick me?")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send("Maybe try kicking someone with a role lower than yours.")
        else:
            await ctx.guild.kick(member)
            await ctx.send(f":white_check_mark: Successfully kicked <@{member.id}>.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Please specify a member.")
        elif member.id == ctx.author.id:
            await ctx.send("Why would you want to ban yourself?")
        elif member.id == self.bot.user.id:
            await ctx.send("Why would you want to ban me?")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send("Maybe try banning someone with a role lower than yours.")
        else:
            logs = discord.utils.get(ctx.guild.text_channels, name="logs")

            await ctx.guild.ban(member)
            await ctx.send(
                f":white_check_mark: Successfully banned <@{member.id}>.\n"
                f"Ban details are in <#{logs.id}>."
            )

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unban(self, ctx, user: discord.User = None):
        if user is None:
            await ctx.send("Please specify a user.")
        elif user.id == ctx.author.id:
            await ctx.send(
                "You're using this command, so you weren't "
                "banned in the first place!"
            )
        elif user.id == self.bot.user.id:
            await ctx.send(
                "I'm responding to this command, so I wasn't "
                "banned in the first place!"
            )
        else:
            try:
                await ctx.guild.unban(user)
            except discord.NotFound:
                await ctx.send(f"**{user}** was never banned.")
            else:
                await ctx.send(
                    f":white_check_mark: Successfully unbanned <@{user.id}>."
                )


def setup(bot):
    bot.add_cog(Admin(bot))
