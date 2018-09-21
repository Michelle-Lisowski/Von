# Procbot Copyright (C) 2018 sirtezza451
# The full license can be found at master/LICENSE

import asyncio
import json
import random
import sys
import traceback

import aiohttp
import discord
from discord.ext import commands

from src.locations import FORTNITE_LOCATIONS

class Random:
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            if str(ctx.command) == 'roll':
                await ctx.send(':x: Please specify a **whole number** of sides.')
            elif str(ctx.command) == 'gay' or 'xp':
                await ctx.send(':x: I could not find that member.')

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(':x: Fetching a picture of a cat failed.')

        else:
            print(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(aliases=['coin_flip'])
    async def flip(self, ctx):
        possibilities = ['Heads', 'Tails']
        result = random.choice(possibilities)
        await ctx.send(':coin: The result is...')

        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.send(f'**{result}**!')

    @commands.command()
    async def roll(self, ctx, number: int = None):
        if not number:
            number = 6
        result = random.randint(1, number)
        await ctx.send(':game_die: The die rolls...')

        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.send(f'**{result}**!')

    @commands.command()
    async def gay(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        if member.id == self.bot.owner_id:
            percentage = 0
            emoji = ':smiley:'
        elif member.id == self.bot.user.id:
            percentage = 0
            emoji = ':smiley:'
        else:
            percentage = random.randint(1, 100)

        if percentage >= 50:
            emoji = ':gay_pride_flag:'
        elif percentage < 50:
            emoji = ':smiley:'
        
        await ctx.send(f'**{member.name}** is {percentage}% gay. {emoji}')

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed()
        embed.title = 'Procbot'
        embed.description = 'Pong! :ping_pong:'
        embed.colour = 0x0000ff
        embed.set_footer(text=f'This took {round(self.bot.latency * 1000)}ms.')
        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://aws.random.cat/meow') as r:
                pic = await r.json()
                embed = discord.Embed()
                embed.title = ':cat: Meow'
                embed.colour = 0x0000ff
                embed.set_image(url=pic['file'])
                await ctx.send(embed=embed)

    @commands.command()
    async def drop(self, ctx):
        destination = random.choice(FORTNITE_LOCATIONS)
        await ctx.send(f':airplane_departure: Next destination: **{destination}**')

    @commands.command()
    @commands.guild_only()
    async def xp(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        if member.bot and member.id != self.bot.user.id:
            await ctx.send(f':information_source: **{member.name}** is a bot! Bots aren\'t invited to the super fancy XP party!')
            return

        else:
            with open('xp.json', 'r') as fp:
                user_xp = json.load(fp)

            if not str(member.id) in user_xp:
                if member.id == self.bot.user.id:
                    user_xp[str(member.id)] = {}
                    user_xp[str(member.id)]['EXPERIENCE'] = int(2 ** 64)
                    user_xp[str(member.id)]['LEVEL'] = 1
                else:
                    user_xp[str(member.id)] = {}
                    user_xp[str(member.id)]['EXPERIENCE'] = 0
                    user_xp[str(member.id)]['LEVEL'] = 1

            with open('xp.json', 'w') as fp:
                json.dump(user_xp, fp, indent=4)            

            embed = discord.Embed()
            embed.title = 'Procbot'
            embed.description = f'Here are **{member.name}**\'s stats.'
            embed.colour = 0x0000ff
            embed.add_field(name='Level', value=user_xp[str(member.id)]['LEVEL'], inline=True)
            embed.add_field(name='XP', value=user_xp[str(member.id)]['EXPERIENCE'], inline=True)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Random(bot))
