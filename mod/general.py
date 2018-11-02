# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import sys

import discord
from discord.ext import commands


class General:
    """
    Command module for general commands.

    List of commands:
    ```
    v!ping
    v!avatar
    v!info
    v!profile
    v!serverinfo
    ```
    """

    def __init__(self, bot):
        self.bot = bot

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
        embed.description = "**Von by sirtezza451#9856**"
        embed.colour = 0x0099FF

        pyver = "{0.major}.{0.minor}.{0.micro}".format(sys.version_info)
        dpyver = "{0.major}.{0.minor}.{0.micro}".format(discord.version_info)
        gitrepo = "https://github.com/sirtezza451/Von"

        embed.add_field(name="Name", value=str(self.bot.user), inline=True)
        embed.add_field(name="ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Server Count", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Version", value="2.0.0-alpha17", inline=True)
        embed.add_field(name="Python Version", value=pyver, inline=True)
        embed.add_field(name="Wrapper Version", value=dpyver, inline=True)
        embed.add_field(name="Source Code", value=gitrepo, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def profile(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed()
        embed.title = member.name
        embed.colour = 0x0099FF
        embed.set_thumbnail(url=member.avatar_url)

        if member.activity is not None:
            atype = self.bot.atype_str(member.activity)
            activity = f"{atype} **{member.activity}**"
        else:
            activity = None

        status = self.bot.status_cap(member.status)

        embed.add_field(name="Name", value=str(member), inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Role", value=member.top_role, inline=True)
        embed.add_field(name="Nickname", value=member.nick, inline=True)
        embed.add_field(name="Status", value=status, inline=True)
        embed.add_field(name="Activity", value=activity, inline=True)
        embed.add_field(name="Account Creation", value=member.created_at, inline=True)
        embed.add_field(name="Joined At", value=member.joined_at, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx, guild: discord.Guild = None):
        embed = discord.Embed()
        embed.title = ctx.guild.name
        embed.colour = 0x0099FF
        embed.set_thumbnail(url=ctx.guild.icon_url)

        textchnls = len(ctx.guild.text_channels)
        vcechnls = len(ctx.guild.voice_channels)
        level = self.bot.level_cap(ctx.guild.verification_level)
        region = self.bot.region_clean(ctx.guild)
        create = ctx.guild.created_at

        embed.add_field(name="Owner", value=str(ctx.guild.owner), inline=True)
        embed.add_field(name="ID", value=ctx.guild.id, inline=True)
        embed.add_field(name="Verification Level", value=level, inline=True)
        embed.add_field(name="Owner ID", value=ctx.guild.owner.id, inline=True)
        embed.add_field(name="Member Count", value=len(ctx.guild.members), inline=True)
        embed.add_field(name="Text Channel Count", value=textchnls, inline=True)
        embed.add_field(name="Role Count", value=len(ctx.guild.roles), inline=True)
        embed.add_field(name="Voice Channel Count", value=vcechnls, inline=True)
        embed.add_field(name="Server Creation", value=create, inline=True)
        embed.add_field(name="Voice Region", value=region, inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
