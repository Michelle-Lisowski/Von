"""
The MIT License (MIT)

Copyright (c) 2018 sirtezza451

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

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
            if str(ctx.command) == 'calculator':
                await ctx.send(':grey_exclamation: Please specify a base number.')
            elif str(ctx.command) == 'cat':
                await ctx.send(':x: Fetching a picture of a cat failed.')

        else:
            print(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(aliases=['coin_flip'])
    async def flip(self, ctx):
        possibilities = ['Heads', 'Tails']
        result = random.choice(possibilities)
        await ctx.send('The result is...')

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

        if int(member.id) == int(self.bot.owner_id):
            percentage = 0
        elif int(member.id) == int(self.bot.user.id):
            percentage = 0
        elif int(member.id) == 292969313961377793:
            percentage = 0
        else:
            percentage = random.randint(1, 100)

        if int(percentage) >= 50:
            emoji = ':gay_pride_flag:'
        else:
            emoji = ':smiley:'

        await ctx.send(f'**{member.name}** is {percentage}% gay. {emoji}')

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed()
        embed.title = 'Jaffa'
        embed.description = 'Pong! :ping_pong:'
        embed.colour = 0x0099ff
        embed.set_footer(text=f'This took {round(self.bot.latency * 1000)}ms.')
        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://aws.random.cat/meow') as r:
                pic = await r.json()
                embed = discord.Embed()
                embed.title = ':cat: Meow'
                embed.colour = 0x0099ff
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
            embed.title = 'Jaffa'
            embed.description = f'Here are **{member.name}**\'s stats.'
            embed.colour = 0x0099ff
            embed.add_field(name='Level', value=user_xp[str(member.id)]['LEVEL'], inline=True)
            embed.add_field(name='XP', value=user_xp[str(member.id)]['EXPERIENCE'], inline=True)
            await ctx.send(embed=embed)

    @commands.command(aliases=['calc'])
    async def calculator(self, ctx, arg1: int = None, operation: str = None, arg2: int = None):
        if operation is None:
            await ctx.send(':grey_exclamation: Please specify an operation. This can be the following:')
            await ctx.send('`+` (add), `-` (subtract), `*` (multiply), `/` (divide), `//` (floor divide) or `**` (exponent)')
        elif arg2 is None:
            await ctx.send(':grey_exclamation: Please specify a second number.')
        else:
            if operation == '+':
                result = arg1 + arg2
            if operation == '-':
                result = arg1 - arg2
            if operation == '*':
                result = arg1 * arg2
            if operation == '/':
                result = arg1 / arg2
            if operation == '//':
                result = arg1 // arg2
            if operation == '**':
                result = arg1 ** arg2
            await ctx.send(f'According to my calculations, the answer is **{result}**.')

def setup(bot):
    bot.add_cog(Random(bot))
