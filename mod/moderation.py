# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.CheckFailure):
            await ctx.send(
                "You require the **Manage Messages** permission to run this command."
            )

    @commands.command()
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
            role = discord.utils.get(ctx.guild.roles, name="Muted")

            if role is None:
                role = await ctx.guild.create_role(name="Muted")

            if role in member.roles:
                await ctx.send(f"<@{member.id}> has already been muted.")
                return

            embed = discord.Embed()
            embed.title = "Mute"
            embed.colour = 0x0099FF

            await self.bot.mute(member)
            embed.add_field(name="Member", value=str(member))
            embed.add_field(name="Member ID", value=member.id)
            embed.add_field(name="Muted By", value=str(ctx.author))
            await ctx.send(embed=embed)

    @commands.command()
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

            if role is None:
                role = await ctx.guild.create_role(name="Muted")

            if not role in member.roles:
                await ctx.send(f"<@{member.id}> was never muted.")
                return

            embed = discord.Embed()
            embed.title = "Unmute"
            embed.colour = 0x0099FF

            await member.remove_roles(role)
            embed.add_field(name="Member", value=str(member))
            embed.add_field(name="Member ID", value=member.id)
            embed.add_field(name="Unmuted By", value=str(ctx.author))
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int = None):
        if number is None:
            await ctx.send("Please specify a number of messages.")
            return

        counter = 0

        async for message in ctx.channel.history(limit=number):
            await message.delete()
            counter += 1

        await ctx.send(f":white_check_mark: Deleted {counter} messages.")


def setup(bot):
    bot.add_cog(Moderation(bot))
