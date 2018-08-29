# Procbot Copyright (C) 2018 sirtezza451
# The full license can be found at master/LICENSE

import datetime
import json

import discord
from discord.ext import commands

class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='help')
    async def help_(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        if ctx.invoked_subcommand is None:
            embed = discord.Embed()
            embed.title = 'Procbot'
            embed.description = f'Get more information by using `{p}help <command>`'
            embed.colour = 0x0000ff
            embed.add_field(name='Music', value=f' `{p}connect` `{p}play` `{p}pause` `{p}resume` `{p}skip` `{p}np` `{p}playlist` `{p}stop` `{p}volume`', inline=False)
            embed.add_field(name='Random', value=f'`{p}roll` `{p}gay` `{p}ping` `{p}cat` `{p}drop` `{p}xp`', inline=False)
            embed.add_field(name='Information', value=f'`{p}info` `{p}profile` `{p}serverinfo`', inline=False)
            embed.add_field(name='Administration', value=f'`{p}kick` `{p}ban` `{p}setting`', inline=False)
            embed.add_field(name='Moderation', value=f'`{p}mute` `{p}unmute` `{p}purge`', inline=False)
            await ctx.send(embed=embed)

    @help_.command()
    async def connect(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}connect'
        embed.description = '**Connects to the specified voice channel**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}connect <voice channel>`', inline=False)
        embed.add_field(name='Example', value=f'`{p}connect Music`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def play(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)        
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}play'
        embed.description = '**Plays a song from YouTube based on the search query**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}play <search query>`', inline=False)
        embed.add_field(name='Example', value=f'`{p}play gods plan`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def pause(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)        
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}pause'
        embed.description = '**Pauses the currently playing music**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}pause`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def resume(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)        
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}resume'
        embed.description = '**Resumes the currently paused music**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}resume`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def skip(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)        
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}skip'
        embed.description = '**Skips the currently playing song**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}skip`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def np(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}np'
        embed.description = '**Displays the currently playing song**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}np`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def playlist(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}playlist'
        embed.description = '**Displays the next 5 songs in the playlist**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}playlist`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def stop(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}stop'
        embed.description = '**Stops the currently playing music**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}stop`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def volume(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}volume'
        embed.description = '**Adjusts the volume or displays the current volume**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}volume <volume>`', inline=False)
        embed.add_field(name='Arguments', value='`volume` - **number** (optional)', inline=False)
        embed.add_field(name='Example', value=f'`{p}volume 75`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def roll(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}roll'
        embed.description = '**Rolls a die with the number of sides specified**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}roll <number of sides>`', inline=False)
        embed.add_field(name='Arguments', value='`number of sides` - **number** (optional)', inline=False)
        embed.add_field(name='Example', value=f'`{p}roll 1234567890`', inline=False)
        embed.set_footer(text='If no number of sides is specified, a 6-sided die will be rolled')
        await ctx.send(embed=embed)

    @help_.command()
    async def gay(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}gay'
        embed.description = '**Tells you how gay the mentioned member is**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}gay <member>`', inline=False)
        embed.add_field(name='Example', value=f'`{p}gay @sirtezza_451#9856`', inline=False)
        embed.set_footer(text='If no member is mentioned, the message returned will display how gay you are')
        await ctx.send(embed=embed)

    @help_.command()
    async def ping(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}ping'
        embed.description = '**Returns Procbot\'s latency in milliseconds**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}ping`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def cat(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}cat'
        embed.description = '**Returns a random picture of a cat**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}cat`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def drop(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}drop'
        embed.description = '**Returns the Fortnite location you should land at**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}drop`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def xp(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}xp'
        embed.description = '**Returns the amount of XP the mentioned member has**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}xp <member>`', inline=False)
        embed.add_field(name='Example', value=f'`{p}xp @sirtezza_451#9856`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def kick(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}kick'
        embed.description = '**Kicks the mentioned member**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}kick <member>`', inline=False)
        embed.add_field(name='Example', value=f'`{p}kick @sirtezza_451#9856`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def ban(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}ban'
        embed.description = '**Bans the mentioned member**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}ban <member>`', inline=False)
        embed.add_field(name='Example', value=f'`{p}ban @sirtezza_451#9856`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def mute(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}mute'
        embed.description = '**Prevents the mentioned member from sending messages**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}mute <member>`', inline=False)
        embed.add_field(name='Example', value=f'`{p}mute @sirtezza_451#9856`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def unmute(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}unmute'
        embed.description = '**Allows the mentioned member to chat again**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}unmute <member>`', inline=False)
        embed.add_field(name='Example', value=f'`{p}unmute @sirtezza_451#9856`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def purge(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}purge'
        embed.description = '**Bulk deletes the specified number of messages**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}purge <number of messages>`', inline=False)
        embed.add_field(name='Arguments', value='`number of messages` - **number**', inline=False)
        embed.add_field(name='Example', value=f'`{p}purge 50`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def info(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}info'
        embed.description = '**Returns information about Procbot**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}info`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def profile(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}profile'
        embed.description = '**Returns information about the mentioned member**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}profile <member>`', inline=False)
        embed.add_field(name='Example', value=f'`{p}profile @sirtezza_451#9856`', inline=False)
        embed.set_footer(text='If no member is mentioned, the message returned will display information about you')
        await ctx.send(embed=embed)

    @help_.command()
    async def serverinfo(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)         
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}serverinfo'
        embed.description = '**Returns information about the current server**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}serverinfo`', inline=False)
        await ctx.send(embed=embed)

    @help_.command()
    async def setting(self, ctx):
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)
        p = guilds[str(ctx.guild.id)]['GUILD_PREFIX']
        embed = discord.Embed()
        embed.title = f'Procbot | {p}setting'
        embed.description = '**Allows you to change various things related to the bot**'
        embed.colour = 0x0000ff
        embed.add_field(name='Usage', value=f'`{p}setting <subcommand> <argument>`', inline=False)
        embed.add_field(name='Example', value=f'`{p}setting prefix -`', inline=False)
        embed.set_footer(text='Using the command with no arguments returns the subcommands that can be used.')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))