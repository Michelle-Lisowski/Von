# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import sys
import time

import discord
from discord.ext import commands


class General:
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.BadArgument):
            await ctx.send("Member not found.")

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed()
        embed.title = self.bot.user.name
        embed.description = ":ping_pong: Pong!"
        embed.colour = 0x0099FF
        embed.set_footer(text=f"This took {latency} ms.")
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed()
        embed.title = member.name
        embed.colour = 0x0099FF
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed()
        embed.title = self.bot.user.name
        embed.description = (
            "**Von by sirtezza451#9856 - made using discord.py rewrite.**"
        )
        embed.colour = 0x0099FF

        pyver = "{0.major}.{0.minor}.{0.micro}".format(sys.version_info)
        dpyver = "{0.major}.{0.minor}.{0.micro}".format(discord.version_info)
        gitrepo = "https://github.com/sirtezza451/Von"

        seconds = time.time() - self.bot.uptime
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        uptime = "{} days, {} hours, {} minutes and {} seconds".format(
            round(days), round(hours), round(minutes), round(seconds)
        )

        embed.add_field(name="Uptime", value=f"Von has been awake for {uptime}.")
        embed.add_field(name="Name", value=self.bot.user)
        embed.add_field(name="ID", value=self.bot.user.id)
        embed.add_field(name="Server Count", value=len(self.bot.guilds))
        embed.add_field(name="Version", value="2.0.0-rc4")
        embed.add_field(name="Python Version", value=pyver)
        embed.add_field(name="Wrapper Version", value=dpyver)
        embed.add_field(name="Source Code", value=gitrepo)
        await ctx.send(embed=embed)

    @commands.command()
    async def profile(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed()
        embed.title = member.name
        embed.colour = 0x0099FF
        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name="Name", value=member)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Role", value=member.top_role)
        embed.add_field(name="Nickname", value=member.nick)
        embed.add_field(name="Status", value=member.status)
        embed.add_field(name="Account Creation", value=member.created_at)
        embed.add_field(name="Joined At", value=member.joined_at)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed()
        embed.title = ctx.guild.name
        embed.colour = 0x0099FF
        embed.set_thumbnail(url=ctx.guild.icon_url)

        textchnls = len(ctx.guild.text_channels)
        vcechnls = len(ctx.guild.voice_channels)
        level = ctx.guild.verification_level
        create = ctx.guild.created_at

        embed.add_field(name="Owner", value=ctx.guild.owner)
        embed.add_field(name="ID", value=ctx.guild.id)
        embed.add_field(name="Verification Level", value=level)
        embed.add_field(name="Owner ID", value=ctx.guild.owner.id)
        embed.add_field(name="Member Count", value=len(ctx.guild.members))
        embed.add_field(name="Text Channel Count", value=textchnls)
        embed.add_field(name="Role Count", value=len(ctx.guild.roles))
        embed.add_field(name="Voice Channel Count", value=vcechnls)
        embed.add_field(name="Server Creation", value=create)
        embed.add_field(name="Voice Region", value=ctx.guild.region)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
